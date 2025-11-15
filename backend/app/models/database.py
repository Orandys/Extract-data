from sqlalchemy import Column, Integer, String, DateTime, Text, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

Base = declarative_base()


def generate_uuid():
    """Generate a UUID string"""
    return str(uuid.uuid4())


class Document(Base):
    __tablename__ = "documents"
    
    id = Column(String, primary_key=True, default=generate_uuid, index=True)
    filename = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="uploaded")  # uploaded, processing, completed, failed
    
    # Relationships
    extractions = relationship("Extraction", back_populates="document", cascade="all, delete-orphan")


class Extraction(Base):
    __tablename__ = "extractions"
    
    id = Column(String, primary_key=True, default=generate_uuid, index=True)
    document_id = Column(String, ForeignKey("documents.id"), nullable=False)
    field_name = Column(String, nullable=False)  # numero_bon, date, client, etc.
    extracted_value = Column(Text)
    confidence = Column(Float)
    bbox = Column(Text)  # JSON string: {"x": 0, "y": 0, "width": 100, "height": 20}
    
    # Relationships
    document = relationship("Document", back_populates="extractions")
    corrections = relationship("Correction", back_populates="extraction", cascade="all, delete-orphan")


class Correction(Base):
    __tablename__ = "corrections"
    
    id = Column(String, primary_key=True, default=generate_uuid, index=True)
    extraction_id = Column(String, ForeignKey("extractions.id"), nullable=False)
    original_value = Column(Text)
    corrected_value = Column(Text)
    bbox = Column(Text)  # JSON string with bounding box coordinates
    correction_date = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    extraction = relationship("Extraction", back_populates="corrections")


class FieldMetrics(Base):
    __tablename__ = "field_metrics"
    
    id = Column(String, primary_key=True, default=generate_uuid, index=True)
    field_name = Column(String, unique=True, nullable=False, index=True)
    total_extractions = Column(Integer, default=0)
    total_corrections = Column(Integer, default=0)
    accuracy = Column(Float, default=100.0)  # (total - corrections) / total * 100
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
