# Backend - Document Extraction API

FastAPI-based backend for extracting data from delivery notes using OCR.

## Features

- Document upload and management
- OCR processing using Tesseract or Doctr
- Automatic field extraction from delivery notes
- Learning from user corrections
- SQLite database for storage

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Install Tesseract OCR:
```bash
# Ubuntu/Debian
sudo apt-get install tesseract-ocr tesseract-ocr-fra

# macOS
brew install tesseract tesseract-lang
```

## Running

1. Make the start script executable:
```bash
chmod +x start.sh
```

2. Start the server:
```bash
./start.sh
```

Or manually:
```bash
python -c "from app.database import init_db; init_db()"
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at http://localhost:8000

## API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### Documents
- `POST /api/documents/upload` - Upload a document
- `GET /api/documents/` - List all documents
- `GET /api/documents/{id}` - Get a specific document
- `DELETE /api/documents/{id}` - Delete a document

### Extraction
- `POST /api/extraction/process/{document_id}` - Process document with OCR
- `GET /api/extraction/document/{document_id}` - Get extractions for a document
- `GET /api/extraction/{id}` - Get specific extraction
- `PUT /api/extraction/{id}` - Update extraction (corrections)

### Learning
- `POST /api/learning/corrections` - Record a correction
- `GET /api/learning/corrections/{field_name}` - Get corrections for a field
- `GET /api/learning/stats` - Get learning statistics

## Database

The application uses SQLite with the following tables:
- `documents` - Uploaded documents
- `extractions` - OCR and extraction results
- `learning_data` - User corrections for learning
