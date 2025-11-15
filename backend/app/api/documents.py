from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import os
import shutil
from datetime import datetime

from app.database import get_db
from app.models.database import Document, Extraction
from app.schemas.schemas import DocumentCreate, DocumentResponse, DocumentWithExtractionsResponse

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# 10MB file size limit
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB in bytes


@router.post("", response_model=DocumentResponse, status_code=201)
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Upload a document for processing
    
    - Accepts PDF and images (JPG, PNG)
    - Max file size: 10MB
    - Returns document metadata with UUID
    """
    
    # Validate file type
    allowed_extensions = ['.pdf', '.png', '.jpg', '.jpeg']
    file_ext = os.path.splitext(file.filename)[1].lower()
    
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"File type not allowed. Allowed types: {allowed_extensions}"
        )
    
    # Read file content to check size
    file_content = await file.read()
    file_size = len(file_content)
    
    if file_size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"File size ({file_size} bytes) exceeds maximum allowed size ({MAX_FILE_SIZE} bytes / 10MB)"
        )
    
    # Create unique filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_filename = f"{timestamp}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, safe_filename)
    
    # Save file
    try:
        with open(file_path, "wb") as buffer:
            buffer.write(file_content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")
    
    # Create document record with UUID
    try:
        document = Document(
            filename=file.filename,
            file_path=file_path,
            status="uploaded"
        )
        
        db.add(document)
        db.commit()
        db.refresh(document)
        
        return document
    except Exception as e:
        # Clean up file if database operation fails
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=f"Failed to create document record: {str(e)}")


@router.get("/{document_id}", response_model=DocumentWithExtractionsResponse)
async def get_document(
    document_id: str,
    db: Session = Depends(get_db)
):
    """Get document with all extractions
    
    Returns document metadata and all extracted fields with bounding boxes
    """
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    return document


@router.delete("/{document_id}")
async def delete_document(
    document_id: str,
    db: Session = Depends(get_db)
):
    """Delete a document and its associated data"""
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # Delete file
    try:
        if os.path.exists(document.file_path):
            os.remove(document.file_path)
    except Exception as e:
        print(f"Failed to delete file: {e}")
    
    # Delete database record (cascades to extractions and corrections)
    try:
        db.delete(document)
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete document: {str(e)}")
    
    return {"message": "Document deleted successfully"}
