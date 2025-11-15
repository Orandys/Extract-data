# Frontend - Document Extraction System

React-based frontend for the document extraction system.

## Features

- Document upload interface
- Real-time OCR processing
- Interactive extraction results
- Field editing and validation
- Responsive design with TailwindCSS

## Tech Stack

- React 18
- Vite
- TailwindCSS
- Axios for API calls
- Fabric.js (for advanced document annotation - optional)
- React-PDF (for PDF viewing - optional)

## Installation

```bash
npm install
```

## Running

Development mode:
```bash
npm run dev
```

The application will be available at http://localhost:5173

## Build

```bash
npm run build
```

## Configuration

Edit `.env` to configure the API URL:
```
VITE_API_URL=http://localhost:8000
```

## Usage

1. Upload a document (PDF or image)
2. Click "Process" to run OCR
3. Review and edit extracted fields
4. Save to validate and improve the system
