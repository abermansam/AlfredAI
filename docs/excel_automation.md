# Excel Automation Module

## Overview
The Excel automation module provides functionality for reading, writing, and manipulating Excel files. It supports automated data entry, formula management, and formatting.

## Components

### ExcelProcessor
Main class for Excel file operations:
```python
class ExcelProcessor:
    def __init__(self, file_path: str):
        """Initialize with Excel file path"""
    
    def read_range(self, sheet: str, range_: str) -> pd.DataFrame:
        """Read data from specified range"""
    
    def write_financial_data(self, data: List[FinancialData], 
                           sheet: str, start_cell: str):
        """Write financial data to Excel"""
    
    def apply_formatting(self, sheet: str, range_: str, 
                        format_type: str):
        """Apply formatting to range"""
```

### Supported Features
- Data reading and writing
- Financial data formatting
- Formula management
- Template handling
- Auto-sizing columns
- Currency formatting

## Usage Example
```python
# Initialize processor
processor = ExcelProcessor("financial_report.xlsx")

# Write financial data
processor.write_financial_data(
    financial_data,
    sheet="Financial Metrics",
    start_cell="A1"
)

# Apply formatting
processor.apply_formatting(
    sheet="Financial Metrics",
    range_="A1:D10",
    format_type="currency"
)
```

## Configuration
- Default currency format: `"$#,##0.00"`
- Default date format: `"yyyy-mm-dd"`
- Auto-size columns: `True` 