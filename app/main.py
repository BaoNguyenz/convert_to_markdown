import os
import uuid
import shutil
import tempfile
import logging
import zipfile
import io
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse
from pydantic import BaseModel, HttpUrl

from app.converter import DoclingConverter

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("docling-main")

app = FastAPI(
    title="Docling Markdown Studio",
    description="Convert documents to high-quality Markdown using IBM's Docling",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request Models
class URLConversionRequest(BaseModel):
    url: str
    enable_ocr: bool = True
    generate_images: bool = False

# Temp dir for uploaded files
TEMP_DIR = tempfile.gettempdir()

# Persistent folder where extracted images are stored and served
# Each conversion gets its own sub-folder named by a short UUID
IMAGES_DIR = Path(os.path.dirname(__file__)) / "images"
IMAGES_DIR.mkdir(exist_ok=True)

# Public base URL for the images static mount
IMAGES_BASE_URL = "http://127.0.0.1:8000/images"

# API Endpoints
@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "service": "Docling Markdown Studio"}

@app.post("/api/convert/file")
async def convert_file(
    file: UploadFile = File(...),
    enable_ocr: bool = Form(True),
    generate_images: bool = Form(False)
):
    """
    Endpoint to upload a local document file and convert it to Markdown.
    """
    logger.info(f"Received file upload: {file.filename}")
    
    # Save uploaded file to a temporary location
    suffix = os.path.splitext(file.filename)[1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
        temp_path = temp_file.name
        try:
            shutil.copyfileobj(file.file, temp_file)
        except Exception as e:
            logger.error(f"Failed to write uploaded file to disk: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to save uploaded file.")
            
    # Process conversion
    try:
        # Create a session-specific sub-folder so multiple conversions don't collide
        session_id = uuid.uuid4().hex[:8] if generate_images else ""

        converter = DoclingConverter(enable_ocr=enable_ocr, generate_images=generate_images)
        result = converter.convert_document(
            temp_path,
            session_id=session_id,
            images_base_url=IMAGES_BASE_URL,
        )

        # Clean up temp file
        os.unlink(temp_path)
        
        if result["success"]:
            # Inject original filename into metadata
            result["metadata"]["filename"] = file.filename
            return result
        else:
            return JSONResponse(status_code=500, content=result)
            
    except Exception as e:
        if os.path.exists(temp_path):
            os.unlink(temp_path)
        logger.error(f"Unexpected error in file conversion endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/convert/url")
async def convert_url(request: URLConversionRequest):
    """
    Endpoint to convert a remote document URL to Markdown.
    """
    logger.info(f"Received URL conversion request: {request.url}")
    
    try:
        # Create a session-specific sub-folder so multiple conversions don't collide
        session_id = uuid.uuid4().hex[:8] if request.generate_images else ""

        converter = DoclingConverter(enable_ocr=request.enable_ocr, generate_images=request.generate_images)
        result = converter.convert_document(
            request.url,
            session_id=session_id,
            images_base_url=IMAGES_BASE_URL,
        )
        
        if result["success"]:
            return result
        else:
            return JSONResponse(status_code=500, content=result)
            
    except Exception as e:
        logger.error(f"Unexpected error in URL conversion endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/download/zip/{session_id}")
async def download_zip(session_id: str):
    """
    Returns a ZIP file containing the markdown and the extracted images folder.
    """
    session_dir = IMAGES_DIR / session_id
    if not session_dir.exists():
        raise HTTPException(status_code=404, detail="Session not found or expired.")
        
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for file_path in session_dir.glob("**/*"):
            if file_path.is_file():
                # Add file to zip using relative path so the structure is preserved
                arcname = file_path.relative_to(session_dir)
                zip_file.write(file_path, arcname)
                
    zip_buffer.seek(0)
    return StreamingResponse(
        zip_buffer, 
        media_type="application/zip", 
        headers={"Content-Disposition": f"attachment; filename=markdown_with_images.zip"}
    )

# Serve extracted images as static files at /images
app.mount("/images", StaticFiles(directory=str(IMAGES_DIR)), name="images")

# Mount frontend static files
static_path = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_path):
    app.mount("/", StaticFiles(directory=static_path, html=True), name="static")
else:
    logger.warning("Static files directory not found. Serving API endpoints only.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
