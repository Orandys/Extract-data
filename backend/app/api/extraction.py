from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.models.database import Document, Extraction, FieldMetrics
from app.schemas.schemas import ExtractionCreate, ExtractionResponse
from app.services.ocr_service import OCRService
from app.services.extraction_service import ExtractionService

router = APIRouter()


@router.post("/process/{document_id}", response_model=List[ExtractionResponse], status_code=201)
async def process_document(
    document_id: str,
    ocr_engine: str = "tesseract",
    db: Session = Depends(get_db)
):
    """Process a document with OCR and extract fields
    
    - Runs OCR (Tesseract or Doctr)
    - Extracts fields using regex patterns
    - Stores text and bounding boxes in SQLite
    - Returns list of extractions with field_name, extracted_value, confidence, bbox
    """
    
    # Get document
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # Update status
    document.status = "processing"
    db.commit()
    
    try:
        # Run OCR
        ocr_service = OCRService(engine=ocr_engine)
        ocr_result = ocr_service.process_document(document.file_path)
        
        # Extract structured data
        extraction_service = ExtractionService()
        extracted_fields = extraction_service.extract_fields(
            ocr_result['text'], 
            bbox_data=ocr_result.get('bbox_data')
        )
        
        # Save extractions to database
        extractions = []
        for field_data in extracted_fields:
            extraction = Extraction(
                document_id=document_id,
                field_name=field_data['field_name'],
                extracted_value=field_data['extracted_value'],
                confidence=field_data['confidence'],
                bbox=field_data['bbox']
            )
            db.add(extraction)
            extractions.append(extraction)
            
            # Update field metrics
            metrics = db.query(FieldMetrics).filter(
                FieldMetrics.field_name == field_data['field_name']
            ).first()
            
            if not metrics:
                metrics = FieldMetrics(
                    field_name=field_data['field_name'],
                    total_extractions=1,
                    total_corrections=0,
                    accuracy=100.0
                )
                db.add(metrics)
            else:
                metrics.total_extractions += 1
                # Recalculate accuracy
                if metrics.total_extractions > 0:
                    metrics.accuracy = ((metrics.total_extractions - metrics.total_corrections) / metrics.total_extractions) * 100
        
        document.status = "completed"
        db.commit()
        
        # Refresh all extractions to get IDs
        for extraction in extractions:
            db.refresh(extraction)
        
        return extractions
        
    except Exception as e:
        document.status = "failed"
        db.commit()
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")


@router.get("/document/{document_id}", response_model=List[ExtractionResponse])
async def get_document_extractions(
    document_id: str,
    db: Session = Depends(get_db)
):
    """Get all extractions for a document"""
    extractions = db.query(Extraction).filter(
        Extraction.document_id == document_id
    ).all()
    return extractions

