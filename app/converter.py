import time
import logging
import uuid
from pathlib import Path
from typing import Dict, Any, Optional

try:
    import torch
    _TORCH_AVAILABLE = True
except ImportError:
    _TORCH_AVAILABLE = False
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.pipeline_options import PdfPipelineOptions, AcceleratorOptions, AcceleratorDevice
from docling.datamodel.base_models import InputFormat
from docling_core.types.doc.base import ImageRefMode

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("docling-converter")

class DoclingConverter:
    """
    Wrapper around IBM's Docling DocumentConverter to provide options,
    logging, and detailed metrics.
    """
    def __init__(self, enable_ocr: bool = True, generate_images: bool = False, images_scale: float = 1.5):
        self.enable_ocr = enable_ocr
        self.generate_images = generate_images
        self.images_scale = images_scale  # Lower = less RAM, default docling is 2.0
        self.converter = self._init_converter()

    def _log_gpu_status(self):
        """
        Logs GPU/CUDA availability and device information.
        """
        if _TORCH_AVAILABLE:
            if torch.cuda.is_available():
                device_count = torch.cuda.device_count()
                device_name = torch.cuda.get_device_name(0)
                torch_version = torch.__version__
                logger.info(f"✅ CUDA is available — PyTorch {torch_version}")
                logger.info(f"   GPU count : {device_count}")
                logger.info(f"   GPU 0     : {device_name}")
            else:
                logger.warning("⚠️  CUDA is NOT available — Docling will run on CPU (slower).")
                logger.warning("    Install a CUDA-enabled PyTorch build to use your GPU.")
        else:
            logger.warning("⚠️  PyTorch is not installed — cannot determine GPU status.")

    def _init_converter(self) -> DocumentConverter:
        """
        Initializes the DocumentConverter with customized pipeline options.
        """
        self._log_gpu_status()
        logger.info("Initializing Docling DocumentConverter...")
        
        # Define pipeline options for PDFs
        pipeline_options = PdfPipelineOptions()

        # Toggle OCR based on parameters
        pipeline_options.do_ocr = self.enable_ocr

        # Setup image generation options — only extract picture images (not full pages)
        pipeline_options.generate_page_images = False
        pipeline_options.generate_picture_images = self.generate_images

        # Rendering scale for PDF pages (lower = less RAM usage, default is 2.0)
        # 1.5 = good quality, ~44% less RAM than default — fixes std::bad_alloc on large docs
        pipeline_options.images_scale = self.images_scale
        logger.info(f"📄 PDF render scale: {self.images_scale}x (lower = less RAM, default=2.0)")

        # Explicit GPU acceleration — use CUDA if available, fall back to CPU
        if _TORCH_AVAILABLE and torch.cuda.is_available():
            pipeline_options.accelerator_options = AcceleratorOptions(
                num_threads=4,
                device=AcceleratorDevice.CUDA
            )
            logger.info("🚀 Docling accelerator set to: CUDA (GPU)")
        else:
            pipeline_options.accelerator_options = AcceleratorOptions(
                num_threads=4,
                device=AcceleratorDevice.CPU
            )
            logger.info("🐢 Docling accelerator set to: CPU")

        # Create the converter — pass pipeline_options via PdfFormatOption
        # Without this, ALL the settings above (OCR, GPU, scale, images) are ignored!
        converter = DocumentConverter(
            format_options={
                InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
            }
        )
        return converter

    def convert_document(self, source: str, session_id: str = "", images_base_url: str = "") -> Dict[str, Any]:
        """
        Converts a document (local path or remote URL) to Markdown.

        Args:
            source:          Local file path or remote URL to convert.
            session_id:      Unique ID for this conversion (used for persistent storage).
            images_base_url: Public URL prefix used to build image src attributes
                             in the markdown (e.g. "http://127.0.0.1:8000/api/download/images").

        Returns:
            A dictionary containing markdown, metadata, and performance metrics.
        """
        start_time = time.time()
        logger.info(f"Starting conversion for source: {source}")

        try:
            # Perform conversion
            result = self.converter.convert(source)

            # --- Image extraction -------------------------------------------
            image_count = 0
            if self.generate_images and session_id:
                # Folder structure:
                # /session_id/
                #   ├── document.md
                #   └── images/
                #       ├── picture-1.png

                from app.main import IMAGES_DIR  # lazy import to avoid circular dependency
                session_dir = IMAGES_DIR / session_id
                images_dir = session_dir / "images"
                images_dir.mkdir(parents=True, exist_ok=True)

                # save_as_markdown() DOES support artifacts_dir (unlike export_to_markdown)
                # It writes the .md file and saves images into artifacts_dir as ./images/picture-N.png
                md_path = session_dir / "document.md"
                result.document.save_as_markdown(
                    filename=md_path,
                    artifacts_dir=images_dir,
                    image_mode=ImageRefMode.REFERENCED,
                )

                # Read it back as a string
                markdown_content = md_path.read_text(encoding="utf-8")

                # Count how many image files were actually saved
                image_count = len(list(images_dir.glob("*.png"))) + len(list(images_dir.glob("*.jpg")))

                # For the API response (frontend display), replace `./images/` with the absolute URL
                if images_base_url:
                    markdown_content = markdown_content.replace(
                        "./images/", f"{images_base_url}/{session_id}/images/"
                    )

                logger.info(f"🖼️  Extracted {image_count} image(s) to: {images_dir}")
            else:
                # No image extraction — placeholders stay as <!-- image -->
                markdown_content = result.document.export_to_markdown()
            # ----------------------------------------------------------------


            # Calculate metrics
            elapsed_time = time.time() - start_time
            logger.info(f"Conversion completed successfully in {elapsed_time:.2f} seconds.")

            # Extract basic metadata
            num_pages = getattr(result.document, "num_pages", 1)
            if hasattr(result, "pages") and result.pages:
                num_pages = len(result.pages)

            return {
                "success": True,
                "markdown": markdown_content,
                "metrics": {
                    "execution_time_sec": round(elapsed_time, 2),
                    "pages_processed": num_pages,
                    "images_extracted": image_count,
                },
                "metadata": {
                    "title": getattr(result.document, "title", "Untitled Document"),
                    "source": source,
                    "session_id": session_id,
                }
            }

        except Exception as e:
            elapsed_time = time.time() - start_time
            logger.error(f"Error during document conversion: {str(e)}", exc_info=True)
            return {
                "success": False,
                "error": str(e),
                "metrics": {
                    "execution_time_sec": round(elapsed_time, 2),
                }
            }

# Quick testing entrypoint
if __name__ == "__main__":
    # Test local conversion
    import sys
    if len(sys.argv) > 1:
        test_source = sys.argv[1]
        conv = DoclingConverter()
        res = conv.convert_document(test_source)
        if res["success"]:
            print("--- CONVERSION SUCCESSFUL ---")
            print(res["markdown"][:500] + "\n...")
        else:
            print(f"--- CONVERSION FAILED: {res['error']} ---")
    else:
        print("Please provide a file path or URL to convert.")
