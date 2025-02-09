"""
Error Handler Module for Excel Operations
"""

from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from datetime import datetime
from loguru import logger

@dataclass
class ExcelError:
    """Represents an Excel operation error"""
    error_type: str
    message: str
    operation: str
    details: Optional[Dict[str, Any]] = None
    timestamp: datetime = datetime.now()

class ExcelErrorHandler:
    """Handles Excel operation errors and provides recovery mechanisms"""
    
    ERROR_TYPES = {
        "validation": "Data validation error",
        "reference": "Cell reference error",
        "formula": "Formula error",
        "permission": "File permission error",
        "backup": "Backup operation error",
        "restore": "Restore operation error"
    }
    
    def __init__(self):
        self.errors: List[ExcelError] = []
    
    def handle_error(self, error_type: str, operation: str, exception: Exception) -> ExcelError:
        """Handle an Excel operation error"""
        error = ExcelError(
            error_type=error_type,
            message=str(exception),
            operation=operation,
            details=self._get_error_details(exception)
        )
        
        self.errors.append(error)
        logger.error(f"{self.ERROR_TYPES[error_type]}: {error.message} in {operation}")
        return error
    
    def _get_error_details(self, exception: Exception) -> Dict[str, Any]:
        """Extract detailed information from the exception"""
        return {
            "exception_type": type(exception).__name__,
            "traceback": str(exception.__traceback__),
            "recoverable": self._is_recoverable(exception)
        }
    
    def _is_recoverable(self, exception: Exception) -> bool:
        """Determine if the error is recoverable"""
        unrecoverable_types = [
            PermissionError,
            FileNotFoundError,
            OSError
        ]
        return not any(isinstance(exception, t) for t in unrecoverable_types)
    
    def get_error_summary(self) -> Dict[str, int]:
        """Get a summary of errors by type"""
        summary = {}
        for error in self.errors:
            summary[error.error_type] = summary.get(error.error_type, 0) + 1
        return summary 