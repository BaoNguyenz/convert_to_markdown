import time
import logging
from typing import Dict, Any, Optional

try:
    import torch
    _TORCH_AVAILABLE = True
except ImportError:
    _TORCH_AVAILABLE = False
from docling.document_converter import DocumentConverter
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.datamodel.base_models import InputFormat

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("docling-converter")

class DoclingConverter:
    """
    Wrapper around IBM's Docling DocumentConverter to provide options,
    logging, and detailed metrics.
    """
    def __init__(self, enable_ocr: bool = True, generate_images: bool = False):
        self.enable_ocr = enable_ocr
        self.generate_images = generate_images
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
        
        # Setup image generation options
        pipeline_options.generate_page_images = self.generate_images
        pipeline_options.generate_picture_images = self.generate_images
        
        # Create the converter with configured options
        converter = DocumentConverter(
            # We can optionally specify custom pipeline options here
        )
        return converter

    def convert_document(self, source: str) -> Dict[str, Any]:
        """
        Converts a document (local path or remote URL) to Markdown.
        Returns a dictionary containing the markdown, metadata, and performance metrics.
        """
        start_time = time.time()
        logger.info(f"Starting conversion for source: {source}")
        
        try:
            # Perform conversion
            result = self.converter.convert(source)
            
            # Export to markdown
            markdown_content = result.document.export_to_markdown()
            
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
                },
                "metadata": {
                    "title": getattr(result.document, "title", "Untitled Document"),
                    "source": source
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
