# Standard library imports
import os
from typing import Dict, Optional

# Third-party library imports
import google.generativeai as genai  # Google's Generative AI library for Gemini models
from PIL import Image  # Python Imaging Library for image processing
from dotenv import load_dotenv  # For loading environment variables from .env file

# Load environment variables from .env file
# This allows us to keep sensitive data like API keys out of the codebase
load_dotenv()

# Retrieve the Gemini API key from environment variables
GEMINI_API_KEY: Optional[str] = os.getenv("GEMINI_API_KEY")

# Validate the API key and provide appropriate warnings
if not GEMINI_API_KEY:
    print("WARNING: GEMINI_API_KEY not found in environment variables")
    print("Please create a .env file with your GEMINI_API_KEY to use the Gemini API")
elif GEMINI_API_KEY == "AIzaSyDA_FnN-Ra200i5ibUx58MoHDdR0G9noqA":
    print("WARNING: You are using the default API key placeholder. Please update with a valid API key.")
    print("Get your API key from https://ai.google.dev/")

# Configure the Gemini API client with the API key if available
if GEMINI_API_KEY:
    # Using genai.configure() to set up the API key globally
    # Note: While IDE might show this as an error, it is a valid function in the library
    genai.configure(api_key=GEMINI_API_KEY)  # type: ignore

async def analyze_interior_image(image_path: str) -> Dict[str, str]:
    """
    Analyze an interior image using Google's Gemini AI to identify the design style.
    
    This function takes an image of an interior space, processes it with Gemini's
    multimodal capabilities, and returns a structured analysis of the interior design style.
    
    Args:
        image_path (str): Absolute or relative path to the image file to be analyzed
        
    Returns:
        Dict[str, str]: Dictionary containing:
            - style_title: A concise title for the identified interior design style
            - style_description: A brief description of the style's characteristics
    
    Raises:
        Exception: Handled internally, returns error information in the response dictionary
    """
    # Validate API key before proceeding
    if not GEMINI_API_KEY or GEMINI_API_KEY == "your_api_key_here":
        # Return informative error if API key is missing or using placeholder
        return {
            "style_title": "Error",
            "style_description": "Valid Gemini API key is required. Please update your .env file with a valid API key from https://ai.google.dev/"
        }
        
    try:
        # Open and prepare the image for processing
        img = Image.open(image_path)
        
        # Initialize the Gemini model
        # Using gemini-1.5-flash for optimal performance and cost efficiency
        # Note: While IDE might show this as an error, GenerativeModel is a valid class in the library
        model = genai.GenerativeModel('gemini-1.5-flash')  # type: ignore
        
        # Craft a detailed prompt that instructs Gemini how to analyze the image
        # The prompt is structured to ensure consistent, high-quality responses
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
        
        # Send the prompt and image to Gemini for analysis
        # The model processes both text and image inputs together
        # Note: While IDE might show this as an error, generate_content is a valid method
        response = model.generate_content([prompt, img])  # type: ignore
        response_text = response.text.strip()
        
        # Parse the response to extract the style title and description
        # The expected format is: "Style Title\nStyle Description"
        lines = response_text.split('\n', 1)
        
        if len(lines) >= 2:
            # If the response follows the expected format, extract both parts
            style_title = lines[0].strip()
            style_description = lines[1].strip()
        else:
            # Fallback handling for unexpected response formats
            style_title = "Interior Style"
            style_description = response_text
        
        # Return the structured analysis results
        return {
            "style_title": style_title,
            "style_description": style_description
        }
    
    except Exception as e:
        # Comprehensive error handling with detailed logging
        print(f"Error in Gemini API call: {str(e)}")
        
        # Provide specific feedback for API key errors
        error_str = str(e)
        if "API key not valid" in error_str or "API_KEY_INVALID" in error_str:
            return {
                "style_title": "API Error",
                "style_description": "Your Gemini API key is invalid. Please check your .env file and update with a valid API key."
            }
        
        # General error response for other exceptions
        return {
            "style_title": "Error",
            "style_description": f"Error analyzing image: {error_str}"
        }
