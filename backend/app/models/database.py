from sqlalchemy import Column, Integer, String, DateTime, Text, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()


class Document(Base):
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    upload_date = Column(DateTime, default=datetime.utcnow)
    document_type = Column(String, default="delivery_note")
    status = Column(String, default="uploaded")  # uploaded, processing, completed, failed
    
    # Relationships
    extractions = relationship("Extraction", back_populates="document")


class Extraction(Base):
    __tablename__ = "extractions"
    
    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    extraction_date = Column(DateTime, default=datetime.utcnow)
    
    # Extracted fields
    delivery_note_number = Column(String)
    delivery_date = Column(String)
    supplier_name = Column(String)
    supplier_address = Column(Text)
    customer_name = Column(String)
    customer_address = Column(Text)
    total_amount = Column(Float)
    currency = Column(String)
    
    # OCR metadata
    ocr_engine = Column(String)  # tesseract or doctr
    confidence_score = Column(Float)
    raw_text = Column(Text)
    
    # Validation
    validated = Column(Integer, default=0)  # 0: not validated, 1: validated
    corrections = Column(Text)  # JSON string of corrections
    
    # Relationships
    document = relationship("Document", back_populates="extractions")


class LearningData(Base):
    __tablename__ = "learning_data"
    
    id = Column(Integer, primary_key=True, index=True)
    extraction_id = Column(Integer, ForeignKey("extractions.id"))
    field_name = Column(String, nullable=False)
    original_value = Column(String)
    corrected_value = Column(String)
    correction_date = Column(DateTime, default=datetime.utcnow)
    pattern = Column(Text)  # Learned pattern for extraction
