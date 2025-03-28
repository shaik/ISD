# Standard library imports
import os

# FastAPI imports
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse

# Environment variable handling
from dotenv import load_dotenv

# Import application routes
from app.routes.upload import router as upload_router

# Load environment variables from .env file
# This makes API keys and other configuration available to the application
load_dotenv()

# Create FastAPI application instance with metadata
app = FastAPI(
    title="Interior Style Detector",
    description="API for detecting interior design styles using Google's Gemini Pro Vision AI",
    version="1.0.0"
)

# Configure Cross-Origin Resource Sharing (CORS)
# This allows the frontend to communicate with the API from different origins
app.add_middleware(
    CORSMiddleware,
    # For production, replace with specific origins for security
    # Example: allow_origins=["https://yourdomain.com"]
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routes
# The upload_router contains endpoints for image upload and analysis
app.include_router(upload_router)

# Mount static files directory to serve frontend assets
# This makes the HTML, CSS, and JavaScript files accessible via HTTP
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Ensure the uploads directory exists for storing user-uploaded images
os.makedirs("app/uploads", exist_ok=True)

# Define root endpoint that redirects to the frontend application
@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Redirect the root URL to the frontend application."""
    return RedirectResponse(url="/static/index.html")

# Entry point for running the application directly (not via Heroku)
if __name__ == "__main__":
    import uvicorn
    
    # Get port from environment variable (for Heroku compatibility) or use default 8000
    port = int(os.getenv("PORT", 8000))
    
    # Start the ASGI server with hot-reloading enabled for development
    uvicorn.run(
        "app.main:app", 
        host="0.0.0.0",  # Accept connections from all network interfaces
        port=port, 
        reload=True  # Enable hot-reloading for development
    )
