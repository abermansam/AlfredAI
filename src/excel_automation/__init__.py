"""
Excel Automation Package

Provides functionality for Excel file operations and automation.
"""

from .excel_handler import ExcelHandler
from .error_handler import ExcelErrorHandler, ExcelError

__all__ = ['ExcelHandler', 'ExcelErrorHandler', 'ExcelError'] 