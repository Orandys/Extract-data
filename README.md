# Extract-data

Document extraction system for delivery notes (bons de livraison) in logistics.

## Overview

This system uses OCR technology to automatically extract structured data from delivery notes, including:
- Numéro de bon (delivery note number)
- Date
- Client (customer name)
- Adresse (address)
- Transporteur (carrier)
- Articles (items)

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
- Axios

## Project Structure

```
backend/
  app/
    main.py           # FastAPI application
    api/              # API routes (documents, extraction, corrections, metrics)
    services/         # Business logic (OCR, extraction)
    models/           # SQLite models (UUID-based)
    schemas/          # Pydantic schemas
  requirements.txt    # Python dependencies

frontend/
  src/
    components/       # React components
    pages/            # Main pages
    services/         # API service layer
  package.json        # Node dependencies
```

## Database Schema

```sql
documents: id (uuid), filename, file_path, uploaded_at, status
extractions: id (uuid), document_id, field_name, extracted_value, confidence, bbox
corrections: id (uuid), extraction_id, original_value, corrected_value, bbox
field_metrics: field_name, total_extractions, total_corrections, accuracy
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

## API Endpoints

### Documents
- `POST /api/documents` - Upload document (max 10MB)
- `GET /api/documents/{id}` - Get document with extractions

### Extraction
- `POST /api/extraction/process/{id}` - Process with OCR (Tesseract or Doctr)
- `GET /api/extraction/document/{id}` - Get all extractions for document

### Corrections
- `POST /api/corrections` - Save user correction with bbox

### Metrics
- `GET /api/metrics` - Get accuracy statistics per field

### Health
- `GET /api/health` - Health check

## Features

- **Document Upload**: Support for PDF, PNG, JPG (max 10MB)
- **Dual OCR Engines**: Choose between Tesseract or Doctr
- **Field Extraction**: Automatic extraction with French-specific patterns
- **Bounding Boxes**: OCR extracts and stores bbox coordinates
- **Corrections**: Track user corrections per field
- **Accuracy Metrics**: Monitor extraction accuracy per field
- **Active Learning**: System improves after 50 corrections per field

## French-Specific Patterns

The system uses regex patterns optimized for French delivery notes:
- `numero_bon`: B[OL][:\s]*[N°#\s]*(\w+[-/]?\w+)
- `date`: Date[:\s]*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})
- `client`: Client[:\s]*([A-Z\s]+)
- `adresse`: Adresse[:\s]*(.+?)
- `transporteur`: Transporteur[:\s]*(.+)
- `articles`: Articles?[:\s]*(.+?)

## Development

See individual README files in `backend/` and `frontend/` directories for detailed development instructions.

## API Documentation

Once the backend is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## License

This is a personal project.
