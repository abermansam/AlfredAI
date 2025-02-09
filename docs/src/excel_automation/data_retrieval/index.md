# Data Retrieval Package

## Overview
The data retrieval package provides the core foundation for retrieving and processing financial data. It defines base classes and interfaces that standardize how financial data is handled across different data sources.

## Components

### Base Module (`base.py`)

#### FinancialData
Core dataclass representing standardized financial data:
```python
@dataclass
class FinancialData:
    source: str        # Source of the data (e.g., "EDGAR", "text")
    date: datetime     # Date of the financial data
    category: str      # Metric category (e.g., "revenue", "total assets")
    value: float       # Numeric value
    confidence: float  # Confidence score (0-1)
    unit: str = "USD"  # Currency unit
    notes: Optional[str] = None  # Additional information
```

#### DataRetriever
Abstract base class for all data retrievers:
```python
class DataRetriever:
    def __init__(self, config=None):
        """Initialize with optional configuration"""
        self.config = config
    
    def extract_from_text(self, text: str) -> List[FinancialData]:
        """Extract financial data from text using pattern matching
        
        Args:
            text: Input text containing financial data
            
        Returns:
            List of extracted FinancialData objects
        """
    
    def validate_data(self, data: FinancialData) -> bool:
        """Validate financial data structure and values
        
        Args:
            data: FinancialData object to validate
            
        Returns:
            True if valid, False otherwise
        """
```

### Package Structure (`__init__.py`)
The package initialization exposes core components:
```python
from .base import DataRetriever, FinancialData

__all__ = ['DataRetriever', 'FinancialData']
```

## Features

### Text Extraction
The base `DataRetriever` implements pattern matching for financial data:
- Recognizes currency values (e.g., "$1.2M", "$500K")
- Extracts categories from context
- Assigns confidence scores
- Standardizes units

### Data Validation
Built-in validation for financial data:
- Positive numeric values
- Valid confidence scores (0-1)
- Required fields presence
- Date format validation
- Unit standardization

## Usage Examples

### Creating Financial Data
```python
from datetime import datetime
from excel_automation.data_retrieval import FinancialData

data = FinancialData(
    source="EDGAR",
    date=datetime.now(),
    category="revenue",
    value=1000000.0,
    confidence=0.95,
    unit="USD",
    notes="Q4 2023"
)
```

### Using the Base Retriever
```python
from excel_automation.data_retrieval import DataRetriever

retriever = DataRetriever()

# Extract from text
text = """
Q2 2024 Financial Results:
Revenue: $1.2M
Operating Expenses: $800K
"""
results = retriever.extract_from_text(text)

# Validate data
for result in results:
    is_valid = retriever.validate_data(result)
    if is_valid:
        print(f"{result.category}: ${result.value:,.2f}")
```

### Implementing Custom Retrievers
```python
from excel_automation.data_retrieval import DataRetriever, FinancialData

class CustomRetriever(DataRetriever):
    def __init__(self, config):
        super().__init__(config)
    
    def extract_from_text(self, text: str) -> List[FinancialData]:
        # Custom implementation
        results = []
        # ... extraction logic ...
        return results
    
    def validate_data(self, data: FinancialData) -> bool:
        # Custom validation rules
        if not super().validate_data(data):
            return False
        # ... additional validation ...
        return True
```

## Integration Points

### With EDGAR Module
The base classes are extended by the EDGAR module:
- `EdgarRetriever` extends `DataRetriever`
- EDGAR data is standardized into `FinancialData`
- Common validation rules are inherited

### With LLM Providers
The base functionality supports LLM integration:
- Text extraction can be enhanced with LLM parsing
- Confidence scores can be adjusted based on LLM certainty
- Validation can incorporate LLM verification

## Error Handling
The base module provides error handling for:
- Invalid data formats
- Type mismatches
- Value range violations
- Missing required fields
- Date parsing errors

## Best Practices
1. Always validate data after extraction
2. Use appropriate confidence scores
3. Include source information
4. Standardize units when possible
5. Add descriptive notes for context 