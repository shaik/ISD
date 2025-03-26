import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
import os
import io
from app.main import app

client = TestClient(app)

@pytest.fixture
def mock_image():
    # Create a simple test image in memory
    return io.BytesIO(b"mock image content")

@pytest.mark.asyncio
async def test_upload_image(mock_image):
    # Mock the Gemini service response
    with patch('app.routes.upload.analyze_interior_image', new_callable=AsyncMock) as mock_analyze:
        mock_analyze.return_value = "This space showcases a minimalist Scandinavian design with clean lines and natural materials."
        
        # Create test file
        files = {
            "file": ("test_image.jpg", mock_image, "image/jpeg")
        }
        
        # Test the upload endpoint
        response = client.post("/upload", files=files)
        
        # Check response
        assert response.status_code == 200
        assert response.json()["success"] is True
        assert "style_description" in response.json()
        assert response.json()["style_description"] == "This space showcases a minimalist Scandinavian design with clean lines and natural materials."
        
        # Verify the mock was called
        mock_analyze.assert_called_once()

def test_upload_invalid_file():
    # Test with non-image file
    files = {
        "file": ("test.txt", io.BytesIO(b"not an image"), "text/plain")
    }
    
    # Test the upload endpoint with invalid file
    response = client.post("/upload", files=files)
    
    # Check response
    assert response.status_code == 400
    assert "File must be an image" in response.text
