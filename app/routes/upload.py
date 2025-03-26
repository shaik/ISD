import os
import uuid
from typing import Dict, Any
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from app.services.gemini_service import analyze_interior_image

router = APIRouter()

UPLOAD_DIR = "app/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload", response_class=JSONResponse)
async def upload_image(file: UploadFile = File(...)) -> Dict[str, Any]:
    """
    Upload an image and get interior style analysis from Gemini
    
    Returns:
        Dict with success status, style_title, style_description, and filename
    """
    # Validate file type
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    try:
        # Generate unique filename
        file_extension = os.path.splitext(file.filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = os.path.join(UPLOAD_DIR, unique_filename)
        
        # Save the file temporarily
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())
        
        # Process with Gemini
        style_result = await analyze_interior_image(file_path)
        
        # Clean up file (optional - remove for debugging)
        # os.remove(file_path)
        
        return {
            "success": True,
            "style_title": style_result["style_title"],
            "style_description": style_result["style_description"],
            "filename": unique_filename
        }
    
    except Exception as e:
        # Log the error in a production environment
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")
