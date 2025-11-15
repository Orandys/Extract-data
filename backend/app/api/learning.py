from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.database import LearningData
from app.schemas.schemas import LearningDataCreate, LearningDataResponse
from app.services.learning_service import LearningService

router = APIRouter()


@router.post("/corrections", response_model=LearningDataResponse)
async def record_correction(
    correction: LearningDataCreate,
    db: Session = Depends(get_db)
):
    """Record a user correction for learning"""
    learning_service = LearningService()
    
    learning_data = learning_service.record_correction(
        db=db,
        extraction_id=correction.extraction_id,
        field_name=correction.field_name,
        original_value=correction.original_value or "",
        corrected_value=correction.corrected_value
    )
    
    return learning_data


@router.get("/corrections/{field_name}", response_model=List[dict])
async def get_corrections(
    field_name: str,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Get corrections for a specific field"""
    learning_service = LearningService()
    suggestions = learning_service.get_learning_suggestions(
        db=db,
        field_name=field_name,
        limit=limit
    )
    return suggestions


@router.get("/stats")
async def get_learning_stats(db: Session = Depends(get_db)):
    """Get learning statistics"""
    
    total_corrections = db.query(LearningData).count()
    
    # Count corrections by field
    corrections_by_field = {}
    all_corrections = db.query(LearningData).all()
    
    for correction in all_corrections:
        field = correction.field_name
        corrections_by_field[field] = corrections_by_field.get(field, 0) + 1
    
    return {
        "total_corrections": total_corrections,
        "corrections_by_field": corrections_by_field,
        "total_fields_learned": len(corrections_by_field)
    }
