import pytesseract
from PIL import Image
from typing import Dict, Optional
import re


class TesseractOCRService:
    """Service for OCR using Tesseract"""
    
    def __init__(self):
        self.engine_name = "tesseract"
    
    def extract_text(self, image_path: str) -> Dict[str, any]:
        """Extract text from image using Tesseract"""
        try:
            image = Image.open(image_path)
            text = pytesseract.image_to_string(image, lang='eng+fra')
            
            # Get confidence score
            data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
            confidences = [int(conf) for conf in data['conf'] if conf != '-1']
            avg_confidence = sum(confidences) / len(confidences) if confidences else 0
            
            return {
                "text": text,
                "confidence": avg_confidence / 100,  # Normalize to 0-1
                "engine": self.engine_name
            }
        except Exception as e:
            raise Exception(f"Tesseract OCR failed: {str(e)}")


class DoctrOCRService:
    """Service for OCR using Doctr"""
    
    def __init__(self):
        self.engine_name = "doctr"
        self.model = None
    
    def _initialize_model(self):
        """Lazy load the doctr model"""
        if self.model is None:
            try:
                from doctr.models import ocr_predictor
                self.model = ocr_predictor(pretrained=True)
            except ImportError:
                raise Exception("Doctr not installed. Please install python-doctr")
    
    def extract_text(self, image_path: str) -> Dict[str, any]:
        """Extract text from image using Doctr"""
        try:
            self._initialize_model()
            from doctr.io import DocumentFile
            
            # Load document
            doc = DocumentFile.from_images(image_path)
            
            # Perform OCR
            result = self.model(doc)
            
            # Extract text and confidence
            text_lines = []
            confidences = []
            
            for page in result.pages:
                for block in page.blocks:
                    for line in block.lines:
                        line_text = " ".join([word.value for word in line.words])
                        text_lines.append(line_text)
                        # Average word confidence in the line
                        line_conf = sum([word.confidence for word in line.words]) / len(line.words) if line.words else 0
                        confidences.append(line_conf)
            
            text = "\n".join(text_lines)
            avg_confidence = sum(confidences) / len(confidences) if confidences else 0
            
            return {
                "text": text,
                "confidence": avg_confidence,
                "engine": self.engine_name
            }
        except Exception as e:
            raise Exception(f"Doctr OCR failed: {str(e)}")


class OCRService:
    """Main OCR service that can use either Tesseract or Doctr"""
    
    def __init__(self, engine: str = "tesseract"):
        self.engine = engine.lower()
        
        if self.engine == "tesseract":
            self.ocr_service = TesseractOCRService()
        elif self.engine == "doctr":
            self.ocr_service = DoctrOCRService()
        else:
            raise ValueError(f"Unknown OCR engine: {engine}")
    
    def process_document(self, image_path: str) -> Dict[str, any]:
        """Process document and extract text"""
        return self.ocr_service.extract_text(image_path)
