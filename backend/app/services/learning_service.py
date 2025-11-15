from typing import Dict, List
from sqlalchemy.orm import Session
from app.models.database import LearningData, Extraction
import json


class LearningService:
    """Service for learning from user corrections"""
    
    def __init__(self):
        self.learned_patterns = {}
    
    def record_correction(
        self,
        db: Session,
        extraction_id: int,
        field_name: str,
        original_value: str,
        corrected_value: str
    ) -> LearningData:
        """Record a user correction for learning"""
        
        # Analyze the correction to learn patterns
        pattern = self._analyze_correction(original_value, corrected_value)
        
        # Save to database
        learning_data = LearningData(
            extraction_id=extraction_id,
            field_name=field_name,
            original_value=original_value,
            corrected_value=corrected_value,
            pattern=json.dumps(pattern) if pattern else None
        )
        
        db.add(learning_data)
        db.commit()
        db.refresh(learning_data)
        
        return learning_data
    
    def _analyze_correction(self, original: str, corrected: str) -> Dict:
        """Analyze correction to learn patterns"""
        if not original or not corrected:
            return {}
        
        pattern_info = {
            'original_length': len(original),
            'corrected_length': len(corrected),
            'edit_distance': self._levenshtein_distance(original, corrected),
            'correction_type': self._classify_correction_type(original, corrected)
        }
        
        return pattern_info
    
    def _levenshtein_distance(self, s1: str, s2: str) -> int:
        """Calculate Levenshtein distance between two strings"""
        if len(s1) < len(s2):
            return self._levenshtein_distance(s2, s1)
        
        if len(s2) == 0:
            return len(s1)
        
        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row
        
        return previous_row[-1]
    
    def _classify_correction_type(self, original: str, corrected: str) -> str:
        """Classify the type of correction"""
        if not original:
            return 'addition'
        if not corrected:
            return 'deletion'
        if original.lower() == corrected.lower():
            return 'case_change'
        if len(original) != len(corrected):
            return 'length_change'
        return 'substitution'
    
    def get_learning_suggestions(
        self,
        db: Session,
        field_name: str,
        limit: int = 10
    ) -> List[Dict]:
        """Get learning suggestions for a field based on past corrections"""
        
        corrections = db.query(LearningData).filter(
            LearningData.field_name == field_name
        ).order_by(
            LearningData.correction_date.desc()
        ).limit(limit).all()
        
        suggestions = []
        for correction in corrections:
            suggestions.append({
                'field_name': correction.field_name,
                'original_value': correction.original_value,
                'corrected_value': correction.corrected_value,
                'pattern': json.loads(correction.pattern) if correction.pattern else None
            })
        
        return suggestions
    
    def apply_learned_patterns(
        self,
        db: Session,
        extraction_data: Dict
    ) -> Dict:
        """Apply learned patterns to improve extraction"""
        
        improved_data = extraction_data.copy()
        
        # For each field, check if we have learned patterns
        for field_name, value in extraction_data.items():
            if value:
                suggestions = self.get_learning_suggestions(db, field_name, limit=5)
                
                # Simple approach: if we see similar patterns, suggest the correction
                for suggestion in suggestions:
                    if suggestion['original_value'] and \
                       self._levenshtein_distance(value, suggestion['original_value']) < 3:
                        # High similarity, might apply the learned correction
                        improved_data[f'{field_name}_suggestion'] = suggestion['corrected_value']
                        break
        
        return improved_data
