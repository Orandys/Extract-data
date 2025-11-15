# API Reference - Updated

Quick reference for the updated API endpoints matching GitHub Copilot instructions.

## Base URL
```
http://localhost:8000
```

## Authentication
Currently no authentication required (can be added for production).

## Endpoints

### 1. Upload Document
Upload a delivery note for processing.

**Endpoint:** `POST /api/documents`

**Request:**
```bash
curl -X POST "http://localhost:8000/api/documents" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@delivery_note.pdf"
```

**Response:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "filename": "delivery_note.pdf",
  "uploaded_at": "2024-01-15T10:30:00",
  "status": "uploaded"
}
```

**Limits:**
- Max file size: 10MB
- Accepted formats: PDF, PNG, JPG, JPEG

---

### 2. Get Document with Extractions
Retrieve document metadata and all extracted fields.

**Endpoint:** `GET /api/documents/{id}`

**Request:**
```bash
curl -X GET "http://localhost:8000/api/documents/550e8400-e29b-41d4-a716-446655440000" \
  -H "accept: application/json"
```

**Response:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "filename": "delivery_note.pdf",
  "uploaded_at": "2024-01-15T10:30:00",
  "status": "completed",
  "extractions": [
    {
      "id": "660e8400-e29b-41d4-a716-446655440001",
      "document_id": "550e8400-e29b-41d4-a716-446655440000",
      "field_name": "numero_bon",
      "extracted_value": "BL-2024-001",
      "confidence": 0.95,
      "bbox": "{\"x\":10,\"y\":20,\"width\":100,\"height\":20}"
    },
    {
      "id": "660e8400-e29b-41d4-a716-446655440002",
      "document_id": "550e8400-e29b-41d4-a716-446655440000",
      "field_name": "date",
      "extracted_value": "15/01/2024",
      "confidence": 0.88,
      "bbox": "{\"x\":10,\"y\":45,\"width\":80,\"height\":18}"
    }
  ]
}
```

---

### 3. Process Document with OCR
Run OCR and extract fields from an uploaded document.

**Endpoint:** `POST /api/extraction/process/{document_id}`

**Parameters:**
- `ocr_engine` (query): "tesseract" or "doctr" (default: "tesseract")

**Request:**
```bash
curl -X POST "http://localhost:8000/api/extraction/process/550e8400-e29b-41d4-a716-446655440000?ocr_engine=tesseract" \
  -H "accept: application/json"
```

**Response:**
```json
[
  {
    "id": "660e8400-e29b-41d4-a716-446655440001",
    "document_id": "550e8400-e29b-41d4-a716-446655440000",
    "field_name": "numero_bon",
    "extracted_value": "BL-2024-001",
    "confidence": 0.95,
    "bbox": "{\"x\":10,\"y\":20,\"width\":100,\"height\":20}"
  },
  {
    "field_name": "date",
    "extracted_value": "15/01/2024",
    "confidence": 0.88,
    "bbox": "{\"x\":10,\"y\":45,\"width\":80,\"height\":18}"
  },
  ...
]
```

**Extracted Fields:**
- `numero_bon` - Delivery note number
- `date` - Date
- `client` - Customer name
- `adresse` - Address
- `transporteur` - Carrier/transporter
- `articles` - Items/articles

---

### 4. Save Correction
Record a user correction for a field extraction.

**Endpoint:** `POST /api/corrections`

**Request:**
```bash
curl -X POST "http://localhost:8000/api/corrections" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{
    "extraction_id": "660e8400-e29b-41d4-a716-446655440001",
    "original_value": "BL-2024-OO1",
    "corrected_value": "BL-2024-001",
    "bbox": "{\"x\":10,\"y\":20,\"width\":100,\"height\":20}"
  }'
```

**Response:**
```json
{
  "id": "770e8400-e29b-41d4-a716-446655440003",
  "extraction_id": "660e8400-e29b-41d4-a716-446655440001",
  "original_value": "BL-2024-OO1",
  "corrected_value": "BL-2024-001",
  "bbox": "{\"x\":10,\"y\":20,\"width\":100,\"height\":20}",
  "correction_date": "2024-01-15T10:35:00"
}
```

**Note:** After 50 corrections for a field, the system triggers active learning to improve extraction patterns.

---

### 5. Get Metrics
Retrieve accuracy statistics for all fields.

**Endpoint:** `GET /api/metrics`

**Request:**
```bash
curl -X GET "http://localhost:8000/api/metrics" \
  -H "accept: application/json"
```

**Response:**
```json
[
  {
    "id": "880e8400-e29b-41d4-a716-446655440004",
    "field_name": "numero_bon",
    "total_extractions": 100,
    "total_corrections": 5,
    "accuracy": 95.0,
    "last_updated": "2024-01-15T10:30:00"
  },
  {
    "id": "880e8400-e29b-41d4-a716-446655440005",
    "field_name": "date",
    "total_extractions": 100,
    "total_corrections": 12,
    "accuracy": 88.0,
    "last_updated": "2024-01-15T10:30:00"
  }
]
```

**Accuracy Formula:** `(total_extractions - total_corrections) / total_extractions * 100`

---

### 6. Health Check
Check if the API is running.

**Endpoint:** `GET /api/health`

**Request:**
```bash
curl -X GET "http://localhost:8000/api/health" \
  -H "accept: application/json"
```

**Response:**
```json
{
  "status": "healthy",
  "service": "document-extraction-api",
  "version": "1.0.0"
}
```

---

### 7. Delete Document
Delete a document and all associated data.

**Endpoint:** `DELETE /api/documents/{id}`

**Request:**
```bash
curl -X DELETE "http://localhost:8000/api/documents/550e8400-e29b-41d4-a716-446655440000" \
  -H "accept: application/json"
```

**Response:**
```json
{
  "message": "Document deleted successfully"
}
```

**Note:** Deletes the document file, extraction records, and correction records (cascade delete).

---

## Error Responses

All endpoints return standard HTTP error codes:

**400 Bad Request:**
```json
{
  "detail": "File size (12582912 bytes) exceeds maximum allowed size (10485760 bytes / 10MB)"
}
```

**404 Not Found:**
```json
{
  "detail": "Document not found"
}
```

**500 Internal Server Error:**
```json
{
  "detail": "Processing failed: Tesseract OCR failed: ..."
}
```

---

## Bounding Box Format

Bounding boxes are stored as JSON strings with pixel coordinates:

```json
{
  "x": 10,
  "y": 20,
  "width": 100,
  "height": 20
}
```

Where:
- `x` - X coordinate (left)
- `y` - Y coordinate (top)
- `width` - Width in pixels
- `height` - Height in pixels

---

## Interactive API Documentation

For interactive API exploration:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
