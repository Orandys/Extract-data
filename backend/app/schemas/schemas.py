from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class DocumentBase(BaseModel):
    filename: str


class DocumentCreate(DocumentBase):
    file_path: str


class DocumentResponse(DocumentBase):
    id: str
    uploaded_at: datetime
    status: str
    
    class Config:
        from_attributes = True


class ExtractionBase(BaseModel):
    field_name: str
    extracted_value: Optional[str] = None
    confidence: Optional[float] = None
    bbox: Optional[str] = None  # JSON string


class ExtractionCreate(ExtractionBase):
    document_id: str


class ExtractionResponse(ExtractionBase):
    id: str
    document_id: str
    
    class Config:
        from_attributes = True


class CorrectionBase(BaseModel):
    original_value: Optional[str] = None
    corrected_value: str
    bbox: Optional[str] = None  # JSON string


class CorrectionCreate(CorrectionBase):
    extraction_id: str


class CorrectionResponse(CorrectionBase):
    id: str
    extraction_id: str
    correction_date: datetime
    
    class Config:
        from_attributes = True


class FieldMetricsResponse(BaseModel):
    id: str
    field_name: str
    total_extractions: int
    total_corrections: int
    accuracy: float
    last_updated: datetime
    
    class Config:
        from_attributes = True


class DocumentWithExtractionsResponse(DocumentResponse):
    """Document response with all extractions"""
    extractions: List[ExtractionResponse] = []
    
    class Config:
        from_attributes = True
