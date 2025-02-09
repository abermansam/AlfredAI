# Excel Handler Documentation

## Overview
The Excel Handler module provides a robust interface for automating Excel operations through Python. It uses xlwings for Excel interaction and includes comprehensive error handling and validation.

## Features
- Automated Excel operations with validation
- Backup and restore functionality
- Dry run mode for testing
- Support for multiple operation types
- Error handling and logging

## Usage

### Basic Setup
```python
from excel_automation import ExcelHandler

# Initialize handler
handler = ExcelHandler(dry_run=False, visible=True)

# Open or create workbook
handler.open_workbook("path/to/workbook.xlsx")
```

### Supported Operations

1. **Cell Updates**
   ```python
   "Update cell A1 to Revenue"
   "Update cell B2 to 100"
   ```

2. **Formatting**
   ```python
   "Format A1:B1 as header with bold text"
   "Set A2:A5 number format to currency"
   ```

3. **Column Operations**
   ```python
   "Set column A width to 15"
   "Delete column B"
   ```

4. **Range Operations**
   ```python
   "Copy range A1:B10 to C1"
   "Clear contents in range D1:D10"
   ```

5. **Formulas and Named Ranges**
   ```python
   "Set B2:B5 formula to =SUM(A2:A5)"
   "Create named range BaseRevenue for A2:A5"
   ```

### Example Usage
```python
instructions = {
    "required_changes": [
        "Update cell A1 to Revenue Projections",
        "Format A1:B1 as header with bold text",
        "Set A2:A5 number format to currency",
        "Set B2:B5 formula to =SUM(A2:A5)*1.1"
    ]
}

handler.apply_changes(instructions)
```

## Error Handling
- Automatic backup creation before changes
- Validation of all operations before execution
- Automatic restore on failure
- Detailed error logging

## Validation
The handler validates:
- Cell reference format and bounds
- Range references
- Formula syntax
- Operation types and parameters

## Backup and Restore
- Automatic backup before changes
- Manual backup creation available
- Restore functionality for failed operations
- Backup directory management

## Configuration
```python
handler = ExcelHandler(
    dry_run=False,  # Set True for validation without changes
    visible=True    # Set False for background operation
)
```

## Best Practices
1. Use dry run mode for testing changes
2. Always check return values for success/failure
3. Handle errors appropriately
4. Use proper cleanup with try/finally blocks

## Example Error Handling
```python
try:
    handler = ExcelHandler(dry_run=False)
    if not handler.open_workbook("workbook.xlsx"):
        raise Exception("Failed to open workbook")
        
    if not handler.apply_changes(instructions):
        raise Exception("Failed to apply changes")
        
finally:
    handler.cleanup()  # Ensures proper cleanup
```

## Limitations
- Single worksheet operations only
- Limited formatting options
- No support for charts or pivot tables
- Excel must be installed on the system

## Technical Details
- Uses xlwings for Excel interaction
- Python 3.6+ required
- Windows/Mac compatible
- Thread-safe operations
