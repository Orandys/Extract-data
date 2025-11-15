from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class DocumentBase(BaseModel):
    filename: str
    document_type: Optional[str] = "delivery_note"


class DocumentCreate(DocumentBase):
    file_path: str


class DocumentResponse(DocumentBase):
    id: int
    upload_date: datetime
    status: str
    
    class Config:
        from_attributes = True


class ExtractionBase(BaseModel):
    delivery_note_number: Optional[str] = None
    delivery_date: Optional[str] = None
    supplier_name: Optional[str] = None
    supplier_address: Optional[str] = None
    customer_name: Optional[str] = None
    customer_address: Optional[str] = None
    total_amount: Optional[float] = None
    currency: Optional[str] = None


class ExtractionCreate(ExtractionBase):
    document_id: int
    ocr_engine: str
    confidence_score: Optional[float] = None
    raw_text: Optional[str] = None


class ExtractionResponse(ExtractionBase):
    id: int
    document_id: int
    extraction_date: datetime
    ocr_engine: str
    confidence_score: Optional[float] = None
    validated: int
    
    class Config:
        from_attributes = True


class ExtractionUpdate(BaseModel):
    delivery_note_number: Optional[str] = None
    delivery_date: Optional[str] = None
    supplier_name: Optional[str] = None
    supplier_address: Optional[str] = None
    customer_name: Optional[str] = None
    customer_address: Optional[str] = None
    total_amount: Optional[float] = None
    currency: Optional[str] = None
    validated: Optional[int] = None
    corrections: Optional[str] = None


class LearningDataCreate(BaseModel):
    extraction_id: int
    field_name: str
    original_value: Optional[str] = None
    corrected_value: str
    pattern: Optional[str] = None


class LearningDataResponse(BaseModel):
    id: int
    extraction_id: int
    field_name: str
    original_value: Optional[str] = None
    corrected_value: str
    correction_date: datetime
    pattern: Optional[str] = None
    
    class Config:
        from_attributes = True
