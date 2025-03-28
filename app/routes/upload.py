# Standard library imports
import os
import uuid
from typing import Dict, Any

# FastAPI imports
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse

# Application imports
from app.services.gemini_service import analyze_interior_image

# Create API router for upload-related endpoints
router = APIRouter()

# Define upload directory and ensure it exists
UPLOAD_DIR = "app/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload", response_class=JSONResponse)
async def upload_image(file: UploadFile = File(...)) -> Dict[str, Any]:
    """
    Upload an interior image and get AI-powered style analysis from Google Gemini.
    
    This endpoint accepts an image file upload, saves it temporarily to the server,
    processes it with the Gemini Vision API to analyze the interior design style,
    and returns the analysis results.
    
    Args:
        file (UploadFile): The uploaded image file from a multipart/form-data request
    
    Returns:
        Dict[str, Any]: JSON response containing:
            - success (bool): Whether the operation was successful
            - style_title (str): The identified interior design style title
            - style_description (str): Description of the identified style
            - filename (str): Unique filename of the saved image
    
    Raises:
        HTTPException: 400 if file is not an image, 500 for processing errors
    """
    # Validate that the uploaded file is an image
    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400, 
            detail="File must be an image. Supported formats include JPEG, PNG, and WebP."
        )
    
    try:
        # Generate a unique filename to prevent collisions
        file_extension = os.path.splitext(file.filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = os.path.join(UPLOAD_DIR, unique_filename)
        
        # Save the uploaded file to the server temporarily
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())
        
        # Process the image with Gemini AI to analyze interior style
        style_result = await analyze_interior_image(file_path)
        
        # Note: File cleanup is commented out for debugging purposes
        # In production, you might want to enable this to save disk space
        # os.remove(file_path)
        
        # Return the analysis results in a structured JSON response
        return {
            "success": True,
            "style_title": style_result["style_title"],
            "style_description": style_result["style_description"],
            "filename": unique_filename
        }
    
    except Exception as e:
        # In a production environment, you would want to log this error
        # to a monitoring system like Sentry or CloudWatch
        print(f"Error processing upload: {str(e)}")
        
        # Return a user-friendly error response
        raise HTTPException(
            status_code=500, 
            detail=f"Error processing image: {str(e)}"
        )
