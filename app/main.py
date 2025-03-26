import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from dotenv import load_dotenv

# Import routes
from app.routes.upload import router as upload_router

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="Interior Style Detector",
    description="API for detecting interior design styles using Gemini Pro Vision",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(upload_router)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Create uploads directory if it doesn't exist
os.makedirs("app/uploads", exist_ok=True)

# Redirect root to index.html
@app.get("/", response_class=HTMLResponse)
async def read_root():
    return RedirectResponse(url="/static/index.html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=int(os.getenv("PORT", 8000)), reload=True)
