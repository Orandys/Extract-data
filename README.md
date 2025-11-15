# Extract-data

Document extraction system for delivery notes (bons de livraison) in logistics.

## Overview

This system uses OCR technology to automatically extract structured data from delivery notes, including:
- Delivery note numbers
- Dates
- Supplier and customer information
- Amounts and other details

The system learns from user corrections to improve extraction accuracy over time.

## Tech Stack

### Backend
- Python 3.10+
- FastAPI
- SQLite
- Tesseract OCR
- Doctr (Deep Learning OCR)

### Frontend
- React 18
- Vite
- TailwindCSS
- Fabric.js (for document annotation)
- React-PDF (for PDF viewing)

## Project Structure

```
backend/
  app/
    main.py           # FastAPI application
    api/              # API routes
    services/         # Business logic (OCR, extraction, learning)
    models/           # SQLite models
    schemas/          # Pydantic schemas
  requirements.txt    # Python dependencies

frontend/
  src/
    components/       # React components
    pages/            # Main pages
    services/         # API service layer
  package.json        # Node dependencies
```

## Quick Start

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Install Tesseract OCR:
```bash
# Ubuntu/Debian
sudo apt-get install tesseract-ocr tesseract-ocr-fra

# macOS
brew install tesseract tesseract-lang
```

4. Start the server:
```bash
chmod +x start.sh
./start.sh
```

Backend will run on http://localhost:8000

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start development server:
```bash
npm run dev
```

Frontend will run on http://localhost:5173

## Features

- **Document Upload**: Support for PDF, PNG, JPG, JPEG, and TIFF files
- **OCR Processing**: Choose between Tesseract or Doctr OCR engines
- **Data Extraction**: Automatic extraction of structured fields from delivery notes
- **Interactive Editing**: Review and correct extracted data
- **Learning System**: System learns from corrections to improve future extractions
- **RESTful API**: Complete API for integration with other systems

## API Documentation

Once the backend is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Development

See individual README files in `backend/` and `frontend/` directories for detailed development instructions.

## License

This is a personal project.
