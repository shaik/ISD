import os
import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    print("WARNING: GEMINI_API_KEY not found in environment variables")
elif GEMINI_API_KEY == "AIzaSyDA_FnN-Ra200i5ibUx58MoHDdR0G9noqA":
    print("WARNING: You are using the default API key placeholder. Please update with a valid API key.")

# Configure Gemini API if key is available
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

from typing import Dict

async def analyze_interior_image(image_path: str) -> Dict[str, str]:
    """
    Analyze an interior image using Gemini
    
    Args:
        image_path (str): Path to the image file
        
    Returns:
        dict: Dictionary containing style_title and style_description
    """
    # Check if API key is valid
    if not GEMINI_API_KEY or GEMINI_API_KEY == "your_api_key_here":
        return {
            "style_title": "Error",
            "style_description": "Valid Gemini API key is required. Please update your .env file with a valid API key from https://ai.google.dev/"
        }
        
    try:
        # Load the image
        img = Image.open(image_path)
        
        # Initialize Gemini model (using newer version as the old one is deprecated)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Create optimized prompt
        prompt = """Describe the interior design style of the room shown in the image.

Respond in this exact format:

[Style Title]
[One or two short sentences (max 30 words) that describe the overall mood and aesthetic of the space.]

Guidelines:

Use a clear, specific style title (2–4 words) such as "Scandinavian Minimalism" or "Industrial Chic".

Focus on the overall design style, not a list of furniture.

Use editorial language (e.g., calm, refined, natural, bold).

Avoid repeating "This room features..." or overly technical phrasing.

Do not exceed 30 words in the description.

Examples:

Modern Minimalism
Clean lines and neutral tones create a calm, uncluttered space with a sleek and elegant feel.

Bohemian Eclectic
Layered textures and colorful decor give this room a warm, creative, and relaxed atmosphere."""
        
        # Generate content
        response = model.generate_content([prompt, img])
        response_text = response.text.strip()
        
        # Parse the response to extract style title and description
        lines = response_text.split('\n', 1)
        
        if len(lines) >= 2:
            style_title = lines[0].strip()
            style_description = lines[1].strip()
        else:
            # Fallback if the response format is unexpected
            style_title = "Interior Style"
            style_description = response_text
        
        # Return structured response
        return {
            "style_title": style_title,
            "style_description": style_description
        }
    
    except Exception as e:
        # Log error in production
        print(f"Error in Gemini API call: {str(e)}")
        
        # Check for API key error
        error_str = str(e)
        if "API key not valid" in error_str or "API_KEY_INVALID" in error_str:
            return {
                "style_title": "API Error",
                "style_description": "Your Gemini API key is invalid. Please check your .env file and update with a valid API key."
            }
        
        return {
            "style_title": "Error",
            "style_description": f"Error analyzing image: {error_str}"
        }
