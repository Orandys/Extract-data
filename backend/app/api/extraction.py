from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.models.database import Document, Extraction
from app.schemas.schemas import ExtractionCreate, ExtractionResponse, ExtractionUpdate
from app.services.ocr_service import OCRService
from app.services.extraction_service import ExtractionService
from app.services.learning_service import LearningService

router = APIRouter()


@router.post("/process/{document_id}", response_model=ExtractionResponse)
async def process_document(
    document_id: int,
    ocr_engine: str = "tesseract",
    db: Session = Depends(get_db)
):
    """Process a document with OCR and extraction"""
    
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
        extracted_fields = extraction_service.extract_fields(ocr_result['text'])
        
        # Apply learning (if available)
        learning_service = LearningService()
        improved_fields = learning_service.apply_learned_patterns(db, extracted_fields)
        
        # Create extraction record
        extraction = Extraction(
            document_id=document_id,
            ocr_engine=ocr_result['engine'],
            confidence_score=ocr_result['confidence'],
            raw_text=ocr_result['text'],
            delivery_note_number=extracted_fields.get('delivery_note_number'),
            delivery_date=extracted_fields.get('delivery_date'),
            supplier_name=extracted_fields.get('supplier_name'),
            supplier_address=extracted_fields.get('supplier_address'),
            customer_name=extracted_fields.get('customer_name'),
            customer_address=extracted_fields.get('customer_address'),
            total_amount=extracted_fields.get('total_amount'),
            currency=extracted_fields.get('currency'),
        )
        
        db.add(extraction)
        document.status = "completed"
        db.commit()
        db.refresh(extraction)
        
        return extraction
        
    except Exception as e:
        document.status = "failed"
        db.commit()
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")


@router.get("/document/{document_id}", response_model=List[ExtractionResponse])
async def get_document_extractions(
    document_id: int,
    db: Session = Depends(get_db)
):
    """Get all extractions for a document"""
    extractions = db.query(Extraction).filter(
        Extraction.document_id == document_id
    ).all()
    return extractions


@router.get("/{extraction_id}", response_model=ExtractionResponse)
async def get_extraction(
    extraction_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific extraction"""
    extraction = db.query(Extraction).filter(Extraction.id == extraction_id).first()
    if not extraction:
        raise HTTPException(status_code=404, detail="Extraction not found")
    return extraction


@router.put("/{extraction_id}", response_model=ExtractionResponse)
async def update_extraction(
    extraction_id: int,
    update_data: ExtractionUpdate,
    db: Session = Depends(get_db)
):
    """Update an extraction (for corrections)"""
    extraction = db.query(Extraction).filter(Extraction.id == extraction_id).first()
    if not extraction:
        raise HTTPException(status_code=404, detail="Extraction not found")
    
    # Track corrections for learning
    learning_service = LearningService()
    
    # Update fields and record corrections
    update_dict = update_data.dict(exclude_unset=True)
    for field, value in update_dict.items():
        if value is not None and hasattr(extraction, field):
            old_value = getattr(extraction, field)
            if old_value != value and field not in ['validated', 'corrections']:
                # Record the correction for learning
                learning_service.record_correction(
                    db=db,
                    extraction_id=extraction_id,
                    field_name=field,
                    original_value=str(old_value) if old_value else "",
                    corrected_value=str(value)
                )
            setattr(extraction, field, value)
    
    db.commit()
    db.refresh(extraction)
    
    return extraction
