from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.database import get_db
from app.models.database import Correction, Extraction, FieldMetrics
from app.schemas.schemas import CorrectionCreate, CorrectionResponse

router = APIRouter()


@router.post("", response_model=CorrectionResponse, status_code=201)
async def save_correction(
    correction: CorrectionCreate,
    db: Session = Depends(get_db)
):
    """Save a user correction for a field extraction
    
    - Records the original and corrected values
    - Updates field metrics and accuracy
    - Triggers learning after 50 corrections
    """
    try:
        # Verify extraction exists
        extraction = db.query(Extraction).filter(Extraction.id == correction.extraction_id).first()
        if not extraction:
            raise HTTPException(status_code=404, detail="Extraction not found")
        
        # Create correction record
        new_correction = Correction(
            extraction_id=correction.extraction_id,
            original_value=correction.original_value,
            corrected_value=correction.corrected_value,
            bbox=correction.bbox
        )
        
        db.add(new_correction)
        
        # Update or create field metrics
        field_name = extraction.field_name
        metrics = db.query(FieldMetrics).filter(FieldMetrics.field_name == field_name).first()
        
        if not metrics:
            metrics = FieldMetrics(
                field_name=field_name,
                total_extractions=1,
                total_corrections=1,
                accuracy=0.0
            )
            db.add(metrics)
        else:
            metrics.total_corrections += 1
            metrics.last_updated = datetime.utcnow()
        
        # Calculate accuracy: (total - corrections) / total * 100
        if metrics.total_extractions > 0:
            metrics.accuracy = ((metrics.total_extractions - metrics.total_corrections) / metrics.total_extractions) * 100
        else:
            metrics.accuracy = 0.0
        
        db.commit()
        db.refresh(new_correction)
        
        # Check if we should trigger active learning (after 50 corrections)
        if metrics.total_corrections >= 50 and metrics.total_corrections % 50 == 0:
            # TODO: Implement active learning to improve extraction rules
            print(f"Active learning trigger: {field_name} has {metrics.total_corrections} corrections")
        
        return new_correction
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to save correction: {str(e)}")
