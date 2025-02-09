"""
Base classes for data retrieval
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List
import re

@dataclass
class FinancialData:
    """Represents extracted financial data"""
    source: str
    date: datetime
    category: str
    value: float
    confidence: float
    unit: str = "USD"
    notes: Optional[str] = None

class DataRetriever:
    """Base class for data retrievers"""
    
    def __init__(self, config=None):
        self.config = config
    
    def extract_from_text(self, text: str) -> List[FinancialData]:
        """Extract financial data from text using simple pattern matching"""
        results = []
        
        # Simple pattern for "$X.XM" or "$X.XK" format
        pattern = r'\$(\d+\.?\d*)([MK])'
        matches = re.finditer(pattern, text)
        
        for match in matches:
            value = float(match.group(1))
            unit_suffix = match.group(2)
            
            # Convert to actual value
            if unit_suffix == 'M':
                value *= 1_000_000
            elif unit_suffix == 'K':
                value *= 1_000
            
            # Try to extract category from the line containing the value
            line = text[max(0, match.start() - 50):min(len(text), match.end() + 50)]
            category = line.split(':')[0].strip().lower() if ':' in line else 'unknown'
            
            financial_data = FinancialData(
                source="text",
                date=datetime.now(),
                category=category,
                value=value,
                confidence=0.8,  # Lower confidence for text extraction
                unit="USD",
                notes="Extracted from text"
            )
            results.append(financial_data)
        
        return results
    
    def validate_data(self, data: FinancialData) -> bool:
        """Validate financial data"""
        try:
            # Basic validation rules
            if data.value <= 0:
                return False
            
            if data.confidence < 0 or data.confidence > 1:
                return False
            
            if not data.category or not data.source:
                return False
            
            if not isinstance(data.date, datetime):
                return False
            
            return True
            
        except Exception:
            return False 