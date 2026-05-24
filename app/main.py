import os
import shutil
import tempfile
import logging
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
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

# Ensure temp directory exists
TEMP_DIR = tempfile.gettempdir()

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
        converter = DoclingConverter(enable_ocr=enable_ocr, generate_images=generate_images)
        result = converter.convert_document(temp_path)
        
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
        converter = DoclingConverter(enable_ocr=request.enable_ocr, generate_images=request.generate_images)
        result = converter.convert_document(request.url)
        
        if result["success"]:
            return result
        else:
            return JSONResponse(status_code=500, content=result)
            
    except Exception as e:
        logger.error(f"Unexpected error in URL conversion endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Mount frontend static files
# Make sure to check if directory exists first
static_path = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_path):
    app.mount("/", StaticFiles(directory=static_path, html=True), name="static")
else:
    logger.warning("Static files directory not found. Serving API endpoints only.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
