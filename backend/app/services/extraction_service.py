import re
from typing import Dict, Optional, List, Tuple
import json


class ExtractionService:
    """Service for extracting structured data from OCR text"""
    
    def __init__(self):
        # French-specific patterns for delivery notes
        self.patterns = {
            "numero_bon": r"B[OL][:\s]*[N°#\s]*(\w+[-/]?\w+)",
            "date": r"Date[:\s]*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})",
            "client": r"Client[:\s]*([A-Z\s]+)",
            "adresse": r"Adresse[:\s]*(.+?)(?=\n\n|\n[A-Z]|$)",
            "transporteur": r"Transporteur[:\s]*(.+)",
            "articles": r"Articles?[:\s]*(.+?)(?=\n\n|Total|$)"
        }
    
    def extract_fields(self, text: str, bbox_data: Optional[List[Dict]] = None) -> List[Dict]:
        """Extract structured fields from text with bounding boxes
        
        Args:
            text: OCR extracted text
            bbox_data: Optional list of bounding box data from OCR
            
        Returns:
            List of extraction dictionaries with field_name, extracted_value, confidence, bbox
        """
        extractions = []
        
        for field_name, pattern in self.patterns.items():
            match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE | re.DOTALL)
            
            if match:
                extracted_value = match.group(1).strip() if match.groups() else match.group(0).strip()
                
                # Try to find bounding box for this match
                bbox = self._find_bbox_for_text(extracted_value, bbox_data) if bbox_data else None
                
                extractions.append({
                    'field_name': field_name,
                    'extracted_value': extracted_value,
                    'confidence': 0.85,  # Default confidence, can be improved with actual OCR confidence
                    'bbox': json.dumps(bbox) if bbox else None
                })
        
        return extractions
    
    def _find_bbox_for_text(self, text: str, bbox_data: List[Dict]) -> Optional[Dict]:
        """Find bounding box coordinates for extracted text
        
        Args:
            text: The extracted text to find bbox for
            bbox_data: List of bbox data from OCR
            
        Returns:
            Dictionary with x, y, width, height or None
        """
        if not bbox_data:
            return None
        
        # Simple implementation: find first bbox that contains the text
        # In production, this should be more sophisticated
        for bbox_item in bbox_data:
            if 'text' in bbox_item and text.lower() in bbox_item['text'].lower():
                return {
                    'x': bbox_item.get('x', 0),
                    'y': bbox_item.get('y', 0),
                    'width': bbox_item.get('width', 0),
                    'height': bbox_item.get('height', 0)
                }
        
        return None
    
    def validate_extraction(self, extracted_data: List[Dict]) -> Dict[str, bool]:
        """Validate extracted data
        
        Args:
            extracted_data: List of extraction dictionaries
            
        Returns:
            Dictionary with validation results for required fields
        """
        validation = {}
        
        # Check required fields
        required_fields = ['numero_bon', 'date', 'client']
        extracted_fields = {item['field_name'] for item in extracted_data if item.get('extracted_value')}
        
        for field in required_fields:
            validation[field] = field in extracted_fields
        
        return validation
