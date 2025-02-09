# Data Retrieval Package

## Overview
The data retrieval package provides base functionality for extracting financial data from various sources. It includes the core data structures and interfaces used throughout the system.

## Components

### FinancialData
A dataclass representing standardized financial data:
```python
@dataclass
class FinancialData:
    source: str        # Data source (e.g., "EDGAR", "text")
    date: datetime     # Date of the financial data
    category: str      # Metric category (e.g., "revenue", "total assets")
    value: float       # Numeric value
    confidence: float  # Confidence score (0-1)
    unit: str = "USD"  # Currency unit
    notes: Optional[str] = None  # Additional information
```

### DataRetriever
Base class for all data retrievers:
```python
class DataRetriever:
    def extract_from_text(self, text: str) -> List[FinancialData]:
        """Extract financial data from text using pattern matching"""
        
    def validate_data(self, data: FinancialData) -> bool:
        """Validate financial data structure and values"""
```

## Usage Examples
```python
# Create financial data
data = FinancialData(
    source="EDGAR",
    date=datetime.now(),
    category="revenue",
    value=1000000.0,
    confidence=0.95,
    unit="USD",
    notes="Q4 2023"
)

# Validate data
retriever = DataRetriever()
is_valid = retriever.validate_data(data)

# Extract from text
text = """
Q2 2024 Financial Results:
Revenue: $1.2M
Operating Expenses: $800K
"""
results = retriever.extract_from_text(text)
``` 