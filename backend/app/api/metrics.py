from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.database import FieldMetrics
from app.schemas.schemas import FieldMetricsResponse

router = APIRouter()


@router.get("", response_model=List[FieldMetricsResponse])
async def get_metrics(db: Session = Depends(get_db)):
    """Get accuracy statistics for all fields
    
    Returns metrics including:
    - Total extractions per field
    - Total corrections per field
    - Accuracy percentage: (total - corrections) / total * 100
    """
    try:
        metrics = db.query(FieldMetrics).all()
        return metrics
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get metrics: {str(e)}")
