# Excel Handler Module

## Overview
The Excel handler module manages all Excel-related operations, including file manipulation, data writing, and formatting.

## Components

### ExcelHandler Class
```python
class ExcelHandler:
    def __init__(self, file_path: str):
        """Initialize Excel handler with file path"""
    
    def read_worksheet(self, sheet_name: str) -> pd.DataFrame:
        """Read worksheet into DataFrame"""
    
    def write_worksheet(self, data: pd.DataFrame, 
                       sheet_name: str,
                       start_cell: str = "A1"):
        """Write DataFrame to worksheet"""
    
    def format_range(self, sheet_name: str,
                    range_: str,
                    format_type: str):
        """Apply formatting to range"""
    
    def add_formula(self, sheet_name: str,
                   cell: str,
                   formula: str):
        """Add Excel formula to cell"""
    
    def save(self):
        """Save changes to Excel file"""
```

### Formatting Options
- Currency formatting
- Date formatting
- Number formatting
- Cell colors and styles
- Conditional formatting

### Formula Support
- Basic arithmetic
- Financial functions
- Lookup functions
- Array formulas 