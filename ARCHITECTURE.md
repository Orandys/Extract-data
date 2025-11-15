# System Architecture

## Overview Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        CLIENT BROWSER                            │
│                                                                  │
│  ┌────────────────────────────────────────────────────────┐    │
│  │           React Frontend (localhost:5173)               │    │
│  │                                                          │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │    │
│  │  │  FileUpload  │  │ DocumentList │  │ExtractionView│ │    │
│  │  │  Component   │  │  Component   │  │  Component   │ │    │
│  │  └──────────────┘  └──────────────┘  └──────────────┘ │    │
│  │                                                          │    │
│  │  ┌────────────────────────────────────────────────┐    │    │
│  │  │        API Service Layer (axios)               │    │    │
│  │  └────────────────────────────────────────────────┘    │    │
│  └────────────────────────────────────────────────────────┘    │
└──────────────────────────┬───────────────────────────────────┬─┘
                          │ HTTP/REST API                      │
                          │                                    │
┌──────────────────────────▼────────────────────────────────────▼─┐
│                  FastAPI Backend (localhost:8000)               │
│                                                                  │
│  ┌────────────────────────────────────────────────────────┐    │
│  │                    API Routes                           │    │
│  │                                                          │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │    │
│  │  │  Documents   │  │  Extraction  │  │   Learning   │ │    │
│  │  │    Router    │  │    Router    │  │    Router    │ │    │
│  │  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘ │    │
│  └─────────┼──────────────────┼──────────────────┼─────────┘    │
│            │                  │                  │              │
│  ┌─────────▼──────────────────▼──────────────────▼─────────┐   │
│  │                    Services Layer                        │   │
│  │                                                           │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │   │
│  │  │     OCR      │  │  Extraction  │  │   Learning   │  │   │
│  │  │   Service    │  │   Service    │  │   Service    │  │   │
│  │  │              │  │              │  │              │  │   │
│  │  │  Tesseract   │  │    Regex     │  │  Corrections │  │   │
│  │  │    Doctr     │  │   Patterns   │  │   Patterns   │  │   │
│  │  └──────────────┘  └──────────────┘  └──────────────┘  │   │
│  └───────────────────────────┬───────────────────────────────┘   │
│                              │                                   │
│  ┌───────────────────────────▼───────────────────────────────┐  │
│  │                   Database Layer                           │  │
│  │                                                             │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │  │
│  │  │  Documents   │  │  Extractions │  │LearningData  │    │  │
│  │  │    Table     │  │    Table     │  │    Table     │    │  │
│  │  └──────────────┘  └──────────────┘  └──────────────┘    │  │
│  │                                                             │  │
│  │              SQLite Database (documents.db)                │  │
│  └─────────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │                    File Storage                              │ │
│  │                  uploads/ directory                          │ │
│  │              (PDF, PNG, JPG, TIFF files)                     │ │
│  └─────────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────┘
```

## Data Flow

### 1. Document Upload Flow
```
User → FileUpload → API Service → POST /api/documents/upload
                                         │
                                         ▼
                                   Save to uploads/
                                         │
                                         ▼
                                   Create Document record
                                         │
                                         ▼
                                   Return Document object
                                         │
                                         ▼
                                   Update DocumentList
```

### 2. OCR Processing Flow
```
User clicks "Process" → ExtractionView → POST /api/extraction/process/{id}
                                                  │
                                                  ▼
                                           OCR Service
                                          /           \
                                    Tesseract       Doctr
                                          \           /
                                           ▼         ▼
                                         Raw text + confidence
                                                  │
                                                  ▼
                                         Extraction Service
                                         (Regex patterns)
                                                  │
                                                  ▼
                                          Extracted fields
                                                  │
                                                  ▼
                                         Learning Service
                                      (Apply learned patterns)
                                                  │
                                                  ▼
                                      Save Extraction record
                                                  │
                                                  ▼
                                      Return to ExtractionView
```

### 3. Learning Flow
```
User edits field → Save → PUT /api/extraction/{id}
                                    │
                                    ▼
                            Compare old vs new values
                                    │
                                    ▼
                            For each changed field:
                                    │
                                    ▼
                         Learning Service records correction
                                    │
                                    ▼
                         Analyze pattern (Levenshtein distance)
                                    │
                                    ▼
                         Save to LearningData table
                                    │
                                    ▼
                         Apply to future extractions
```

## Component Interaction

### Frontend Components
```
HomePage
  │
  ├─── FileUpload
  │      └─── documentsAPI.upload()
  │
  ├─── DocumentList
  │      ├─── documentsAPI.list()
  │      └─── documentsAPI.delete()
  │
  └─── ExtractionView
         ├─── extractionAPI.process()
         ├─── extractionAPI.getByDocument()
         └─── extractionAPI.update()
```

### Backend Services
```
API Routes
  │
  ├─── Documents Router
  │      └─── File I/O
  │
  ├─── Extraction Router
  │      ├─── OCR Service
  │      │      ├─── Tesseract
  │      │      └─── Doctr
  │      │
  │      ├─── Extraction Service
  │      │      └─── Regex patterns
  │      │
  │      └─── Learning Service
  │             ├─── Record corrections
  │             └─── Apply patterns
  │
  └─── Learning Router
         └─── Learning Service
                ├─── Get corrections
                └─── Statistics
```

## Database Schema Relationships

```
┌─────────────────┐
│   Documents     │
│ ──────────────  │
│ id (PK)         │◄────┐
│ filename        │     │
│ file_path       │     │
│ upload_date     │     │
│ status          │     │
└─────────────────┘     │
                        │ 1:N
                        │
                   ┌────┴────────────┐
                   │   Extractions   │
                   │ ─────────────── │
                   │ id (PK)         │◄────┐
                   │ document_id (FK)│     │
                   │ extraction_date │     │
                   │ [extracted data]│     │
                   │ confidence      │     │
                   └─────────────────┘     │
                                           │ 1:N
                                           │
                                      ┌────┴────────────┐
                                      │ LearningData    │
                                      │ ─────────────── │
                                      │ id (PK)         │
                                      │ extraction_id(FK)│
                                      │ field_name      │
                                      │ original_value  │
                                      │ corrected_value │
                                      │ pattern         │
                                      └─────────────────┘
```

## Technology Stack Layers

```
┌──────────────────────────────────────────┐
│         Presentation Layer                │
│  React, TailwindCSS, Axios                │
└──────────────────┬───────────────────────┘
                   │ HTTP/JSON
┌──────────────────▼───────────────────────┐
│         Application Layer                 │
│  FastAPI, Pydantic, CORS                  │
└──────────────────┬───────────────────────┘
                   │
┌──────────────────▼───────────────────────┐
│         Business Logic Layer              │
│  OCR, Extraction, Learning Services       │
└──────────────────┬───────────────────────┘
                   │
┌──────────────────▼───────────────────────┐
│         Data Access Layer                 │
│  SQLAlchemy ORM                           │
└──────────────────┬───────────────────────┘
                   │
┌──────────────────▼───────────────────────┐
│         Data Storage Layer                │
│  SQLite + File System                     │
└──────────────────────────────────────────┘
```

## External Dependencies

```
┌─────────────────────────────────────────┐
│          System Dependencies             │
├─────────────────────────────────────────┤
│  • Tesseract OCR (system package)       │
│  • Language packs (eng, fra)            │
│  • Python 3.10+                          │
│  • Node.js 16+                           │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│       Python Dependencies                │
├─────────────────────────────────────────┤
│  • FastAPI (web framework)               │
│  • Uvicorn (ASGI server)                 │
│  • SQLAlchemy (ORM)                      │
│  • Pytesseract (OCR wrapper)             │
│  • Pillow (image processing)             │
│  • python-doctr (deep learning OCR)      │
│  • Pydantic (validation)                 │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│       Node.js Dependencies               │
├─────────────────────────────────────────┤
│  • React (UI library)                    │
│  • Vite (build tool)                     │
│  • TailwindCSS (styling)                 │
│  • Axios (HTTP client)                   │
│  • Fabric.js (canvas manipulation)       │
│  • React-PDF (PDF viewing)               │
└─────────────────────────────────────────┘
```
