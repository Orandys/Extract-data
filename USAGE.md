# Usage Guide

This guide explains how to use the Document Extraction System.

## Getting Started

### Prerequisites

**For Backend:**
- Python 3.10 or higher
- Tesseract OCR installed on your system
- pip package manager

**For Frontend:**
- Node.js 16 or higher
- npm package manager

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/Orandys/Extract-data.git
cd Extract-data
```

2. **Set up the backend**
```bash
cd backend
pip install -r requirements.txt
```

3. **Install Tesseract OCR**

Ubuntu/Debian:
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr tesseract-ocr-fra
```

macOS:
```bash
brew install tesseract tesseract-lang
```

Windows:
- Download from: https://github.com/UB-Mannheim/tesseract/wiki
- Add to PATH

4. **Set up the frontend**
```bash
cd ../frontend
npm install
```

## Running the Application

### Start Backend Server

```bash
cd backend
chmod +x start.sh
./start.sh
```

Or manually:
```bash
cd backend
python -c "from app.database import init_db; init_db()"
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The backend will run on: http://localhost:8000

API Documentation available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Start Frontend Application

In a new terminal:
```bash
cd frontend
npm run dev
```

The frontend will run on: http://localhost:5173

## Using the System

### 1. Upload a Document

1. Open http://localhost:5173 in your browser
2. Click "Choose File" in the Upload Document section
3. Select a delivery note (PDF or image file)
4. Click "Upload"

The document will be uploaded and appear in the Documents list.

### 2. Process Document with OCR

1. Click "View" on any uploaded document
2. Choose one of the processing options:
   - **Process with Tesseract**: Fast, works well with printed text
   - **Process with Doctr**: More advanced, better for complex layouts
3. Wait for processing to complete

### 3. Review and Edit Extracted Data

After processing, you'll see extracted fields:
- Delivery Note Number
- Delivery Date
- Supplier Name and Address
- Customer Name and Address
- Total Amount
- Currency

To edit:
1. Click "Edit & Validate"
2. Correct any incorrect fields
3. Click "Save"

The system will learn from your corrections!

### 4. Learning System

When you correct extraction errors, the system:
- Records the original and corrected values
- Analyzes patterns in corrections
- Applies learned patterns to future extractions
- Improves accuracy over time

## API Usage

### Upload a Document

```bash
curl -X POST "http://localhost:8000/api/documents/upload" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/delivery_note.pdf"
```

### Process Document

```bash
curl -X POST "http://localhost:8000/api/extraction/process/1?ocr_engine=tesseract" \
  -H "accept: application/json"
```

### List Documents

```bash
curl -X GET "http://localhost:8000/api/documents/" \
  -H "accept: application/json"
```

### Get Extraction Results

```bash
curl -X GET "http://localhost:8000/api/extraction/document/1" \
  -H "accept: application/json"
```

### Update/Correct Extraction

```bash
curl -X PUT "http://localhost:8000/api/extraction/1" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{
    "delivery_note_number": "BL-2024-001",
    "delivery_date": "2024-01-15",
    "validated": 1
  }'
```

### Get Learning Statistics

```bash
curl -X GET "http://localhost:8000/api/learning/stats" \
  -H "accept: application/json"
```

## Supported File Formats

- **PDF** (.pdf)
- **PNG** (.png)
- **JPEG** (.jpg, .jpeg)
- **TIFF** (.tiff)

## Extracted Fields

The system attempts to extract the following fields from delivery notes:

1. **Delivery Note Number**: Unique identifier for the delivery
2. **Delivery Date**: Date of delivery
3. **Supplier Name**: Name of the supplying company
4. **Supplier Address**: Full address of supplier
5. **Customer Name**: Name of the receiving company
6. **Customer Address**: Full address of customer
7. **Total Amount**: Total monetary amount
8. **Currency**: Currency code (EUR, USD, etc.)

## Tips for Best Results

1. **Image Quality**: Use high-resolution scans (300 DPI or higher)
2. **File Format**: PDF or TIFF generally work better than JPEG
3. **Language**: System works best with English and French text
4. **Corrections**: Always validate and correct extracted data to improve the learning system
5. **OCR Engine**: 
   - Use Tesseract for standard printed documents
   - Use Doctr for handwritten or complex layouts

## Troubleshooting

### Backend won't start
- Check Python version: `python3 --version` (should be 3.10+)
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check if port 8000 is available

### Frontend won't start
- Check Node version: `node --version` (should be 16+)
- Delete node_modules and reinstall: `rm -rf node_modules && npm install`
- Check if port 5173 is available

### OCR not working
- Verify Tesseract is installed: `tesseract --version`
- Check Tesseract language packs: `tesseract --list-langs`
- For Doctr, ensure TensorFlow is properly installed

### Poor extraction quality
- Improve image quality
- Try different OCR engine
- Correct extracted data to train the system
- Check if document format matches expected delivery note structure

## Development

### Backend Development
```bash
cd backend
# Run in development mode with auto-reload
uvicorn app.main:app --reload
```

### Frontend Development
```bash
cd frontend
# Run in development mode with hot reload
npm run dev
```

### Build for Production
```bash
# Frontend
cd frontend
npm run build

# Backend - use a production ASGI server
pip install gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

## Support

For issues or questions:
- Check the API documentation at http://localhost:8000/docs
- Review logs in the terminal
- Check the README files in backend/ and frontend/ directories
