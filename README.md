# Interior Style Detector

A full-stack web application that uses Gemini Pro Vision to analyze and describe interior design styles from uploaded images.

## Features

- Upload images of interior spaces
- AI-powered analysis using Google's Gemini Pro Vision API
- Clean, responsive UI with drag-and-drop functionality
- Real-time style description in 1-2 engaging sentences

## Tech Stack

- **Backend**: Python with FastAPI
- **Frontend**: HTML, CSS, JavaScript
- **AI**: Google Gemini Pro Vision API
- **Deployment**: Heroku-ready configuration

## Project Structure

```
app/
├── main.py              # FastAPI application entry point
├── routes/              # API routes
│   └── upload.py        # Image upload endpoint
├── services/            # Business logic
│   └── gemini_service.py # Gemini API integration
├── static/              # Frontend files
│   ├── index.html       # Main HTML page
│   ├── styles.css       # CSS styles
│   └── app.js           # Frontend JavaScript
├── tests/               # Test files
│   └── test_upload.py   # Tests for upload endpoint
└── uploads/             # Temporary storage for uploaded images
```

## Setup and Installation

### Prerequisites

- Python 3.11+
- Google Gemini API key

### Local Development

1. Clone the repository:
   ```
   git clone <repository-url>
   cd interior-style-detector
   ```

2. Create a virtual environment and install dependencies:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root and add your Gemini API key:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```

4. Run the application:
   ```
   uvicorn app.main:app --reload
   ```

5. Open your browser and navigate to `http://localhost:8000/static/index.html`

### Running Tests

```
pytest app/tests/
```

## Deployment to Heroku

1. Create a Heroku app:
   ```
   heroku create your-app-name
   ```

2. Set the Gemini API key as a config variable:
   ```
   heroku config:set GEMINI_API_KEY=your_api_key_here
   ```

3. Deploy to Heroku:
   ```
   git push heroku main
   ```

4. Open the app:
   ```
   heroku open
   ```

## Usage

1. Open the application in your browser
2. Drag and drop an image of an interior space or click to browse files
3. Click "Analyze Interior Style"
4. View the AI-generated description of the interior design style

## License

MIT

## Acknowledgements

- Google Gemini Pro Vision API
- FastAPI framework
- Heroku for hosting
