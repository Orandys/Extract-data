import re
from typing import Dict, Optional


class ExtractionService:
    """Service for extracting structured data from OCR text"""
    
    def __init__(self):
        # Define patterns for extraction
        self.patterns = {
            'delivery_note_number': [
                r'(?:bon|note|n°|num(?:ero)?|#)\s*(?:de\s*)?(?:livraison)?\s*:?\s*([A-Z0-9\-]+)',
                r'delivery\s*note\s*(?:number|no|#)?\s*:?\s*([A-Z0-9\-]+)',
            ],
            'delivery_date': [
                r'date\s*(?:de\s*livraison)?\s*:?\s*(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})',
                r'(?:date|delivered)\s*:?\s*(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})',
            ],
            'supplier_name': [
                r'(?:fournisseur|supplier|from)\s*:?\s*([A-Z][A-Za-z\s\&\.]+)',
            ],
            'customer_name': [
                r'(?:client|customer|to|destinataire)\s*:?\s*([A-Z][A-Za-z\s\&\.]+)',
            ],
            'total_amount': [
                r'(?:total|montant)\s*:?\s*([0-9,\.]+)',
                r'(?:total|amount)\s*:?\s*\$?\s*([0-9,\.]+)',
            ],
            'currency': [
                r'(?:total|montant)\s*:?\s*[0-9,\.]+\s*([A-Z]{3})',
                r'\$|USD|EUR|GBP|CAD',
            ]
        }
    
    def extract_fields(self, text: str) -> Dict[str, Optional[str]]:
        """Extract structured fields from text"""
        extracted = {}
        
        for field, patterns in self.patterns.items():
            value = None
            for pattern in patterns:
                match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
                if match:
                    if match.groups():
                        value = match.group(1).strip()
                    else:
                        value = match.group(0).strip()
                    break
            extracted[field] = value
        
        # Extract supplier and customer addresses (multi-line)
        extracted['supplier_address'] = self._extract_address(text, 'supplier')
        extracted['customer_address'] = self._extract_address(text, 'customer')
        
        # Parse amount to float
        if extracted.get('total_amount'):
            try:
                amount_str = extracted['total_amount'].replace(',', '.')
                extracted['total_amount'] = float(amount_str)
            except ValueError:
                extracted['total_amount'] = None
        
        return extracted
    
    def _extract_address(self, text: str, address_type: str) -> Optional[str]:
        """Extract address from text"""
        # Simple heuristic: look for lines after supplier/customer name
        keywords = {
            'supplier': ['fournisseur', 'supplier', 'from'],
            'customer': ['client', 'customer', 'to', 'destinataire']
        }
        
        lines = text.split('\n')
        address_lines = []
        capture = False
        
        for i, line in enumerate(lines):
            line_lower = line.lower()
            
            # Check if this line contains the keyword
            if any(kw in line_lower for kw in keywords.get(address_type, [])):
                capture = True
                continue
            
            # Capture next few lines as address
            if capture and line.strip():
                # Stop if we hit another section
                if any(kw in line_lower for kw in ['date', 'total', 'items', 'products', 'quantity']):
                    break
                address_lines.append(line.strip())
                if len(address_lines) >= 3:  # Usually address is 2-3 lines
                    break
        
        return '\n'.join(address_lines) if address_lines else None
    
    def validate_extraction(self, extracted_data: Dict) -> Dict[str, bool]:
        """Validate extracted data"""
        validation = {}
        
        # Check required fields
        required_fields = ['delivery_note_number', 'delivery_date']
        for field in required_fields:
            validation[field] = bool(extracted_data.get(field))
        
        return validation
