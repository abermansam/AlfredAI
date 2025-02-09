"""
Excel Handler Module

Handles Excel file operations and modifications based on parsed instructions.
"""

import xlwings as xw
from typing import Dict, List, Optional, Union, Tuple, Any
from loguru import logger
import re
from dataclasses import dataclass
from datetime import datetime
import os
import platform
from .mac_helper import launch_excel_macos
from enum import Enum

class OperationType(Enum):
    """Types of Excel operations"""
    UPDATE = "update"
    FORMULA = "formula"
    COPY = "copy"
    FORMAT = "format"
    NUMBER_FORMAT = "number_format"
    COLUMN_WIDTH = "column_width"
    CLEAR = "clear"
    INSERT_ROW = "insert_row"
    DELETE_COLUMN = "delete_column"
    NAMED_RANGE = "named_range"

@dataclass
class ExcelChange:
    """Represents a single Excel change operation with validation status"""
    operation: OperationType
    target: str
    value: Any
    status: str = "pending"
    error: Optional[str] = None
    timestamp: datetime = datetime.now()

class ExcelHandler:
    def __init__(self, dry_run: bool = False, visible: bool = True):
        self.workbook = None
        self.app = None
        self.active_sheet = None
        self.dry_run = dry_run
        self.change_history: List[ExcelChange] = []
        self._backup_path: Optional[str] = None
        self.visible = visible
    
    def _initialize_excel(self) -> bool:
        """Initialize Excel application with proper settings"""
        try:
            # Try to connect to running Excel instance
            self.app = xw.apps.active
            if not self.app:
                # Only create new instance if needed
                self.app = xw.App(visible=self.visible)
            
            logger.info("Excel initialized successfully")
            return True

        except Exception as e:
            logger.error(f"Failed to initialize Excel: {str(e)}")
            self.app = None  # Just clear the reference
            return False

    def open_workbook(self, file_path: str) -> bool:
        """Open an Excel workbook or create new if doesn't exist."""
        try:
            if not self.app and not self._initialize_excel():
                return False

            file_path = os.path.abspath(file_path)  # Use absolute path
            
            # Close any open workbook first
            if self.workbook:
                self.workbook.close()
                self.workbook = None

            if os.path.exists(file_path):
                self.workbook = self.app.books.open(file_path)
            else:
                # Create new workbook
                self.workbook = self.app.books.add()
                self.workbook.save(file_path)
            
            self.active_sheet = self.workbook.sheets.active
            self.workbook.activate()  # Make sure this workbook is visible
            return True
            
        except Exception as e:
            logger.error(f"Error opening workbook: {str(e)}")
            return False
    
    def _parse_cell_reference(self, cell_ref: str) -> Tuple[str, Union[int, str]]:
        """Parse and validate cell reference"""
        # Handle column-only references (e.g., 'A:A')
        if ':' in cell_ref:
            return cell_ref.split(':')
        
        # Handle row-only references (e.g., '5:5')
        if cell_ref.isdigit():
            row_num = int(cell_ref)
            if row_num < 1 or row_num > 1048576:  # Excel's max row
                raise ValueError(f"Invalid row number: {row_num}")
            return (cell_ref, cell_ref)
        
        # Handle single column (e.g., 'A')
        if cell_ref.isalpha():
            if len(cell_ref) > 3:  # Excel's max column is XFD
                raise ValueError(f"Invalid column reference: {cell_ref}")
            return (cell_ref, cell_ref)
        
        # Handle normal cell references (e.g., 'A1')
        match = re.match(r"([A-Z]+)([0-9]+)", cell_ref)
        if not match:
            raise ValueError(f"Invalid cell reference format: {cell_ref}")
        
        col, row = match.groups()
        row_num = int(row)
        
        # Validate column and row
        if len(col) > 3:  # Excel's max column is XFD
            raise ValueError(f"Invalid column reference: {col}")
        if row_num < 1 or row_num > 1048576:  # Excel's max row
            raise ValueError(f"Invalid row number: {row_num}")
        
        return (col, row)

    def create_backup(self) -> bool:
        """Create a backup by copying current file to backup location"""
        try:
            if self.workbook:
                current_file = os.path.abspath(self.workbook.fullname)
                backup_dir = os.path.abspath(os.path.join("output", "backups"))
                backup_path = os.path.abspath(os.path.join(backup_dir, "current_backup.xlsx"))
                
                # Save current workbook first
                self.workbook.save()
                
                # Copy current file to backup location
                import shutil
                shutil.copy2(current_file, backup_path)
                self._backup_path = backup_path
                
                logger.debug(f"Created backup at {backup_path}")
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to create backup: {str(e)}")
            return False

    def cleanup(self) -> None:
        """Clean up workbook and ensure final backup exists"""
        try:
            if self.workbook:
                # Create final backup before closing
                self.create_backup()
                self.workbook.close()
                self.workbook = None
        except Exception as e:
            logger.error(f"Error during cleanup: {str(e)}")

    def validate_changes(self, changes: List[str]) -> List[ExcelChange]:
        """Validate proposed changes before applying them"""
        validated_changes = []
        
        for change in changes:
            try:
                # First try to parse the instruction
                excel_change = self._parse_change_instruction(change)
                
                if excel_change:
                    # For valid instruction format, validate the cell references
                    try:
                        if ":" in excel_change.target:
                            if " to " in excel_change.target:
                                source, target = excel_change.target.split(" to ")
                                self._parse_cell_reference(source.split(":")[0])
                                self._parse_cell_reference(target)
                            else:
                                start, end = excel_change.target.split(":")
                                self._parse_cell_reference(start)
                                self._parse_cell_reference(end)
                        else:
                            self._parse_cell_reference(excel_change.target)
                        
                        excel_change.status = "valid"
                        
                    except ValueError as e:
                        # Invalid cell reference
                        excel_change.status = "error"
                        excel_change.error = str(e)
                else:
                    # Invalid instruction format
                    excel_change = ExcelChange(
                        operation=OperationType.UPDATE,
                        target="",
                        value="",
                        status="error",
                        error="Invalid instruction format"
                    )
                
                validated_changes.append(excel_change)
                
            except Exception as e:
                # Unexpected error during validation
                excel_change = ExcelChange(
                    operation=OperationType.UPDATE,
                    target="",
                    value="",
                    status="error",
                    error=f"Validation error: {str(e)}"
                )
                validated_changes.append(excel_change)
        
        return validated_changes

    def apply_changes(self, instructions: Dict) -> bool:
        """Apply a set of changes to the workbook"""
        try:
            changes = instructions.get('required_changes', [])
            if not changes:
                logger.warning("No changes provided")
                return True

            current_file = os.path.abspath(self.workbook.fullname)
            
            # Create backup of current state before changes
            if os.path.exists(current_file):
                if not self.create_backup():
                    logger.error("Failed to create backup, aborting changes")
                    return False

            # Validate and apply changes
            validated_changes = self.validate_changes(changes)
            if not all(change.status == "valid" for change in validated_changes):
                logger.error("Validation failed for some changes:")
                for change in validated_changes:
                    if change.status == "error":
                        logger.error(f"- {change.operation} {change.target}: {change.error}")
                return False

            # Apply changes to current file
            if not self.dry_run:
                success = self._apply_validated_changes(validated_changes)
                if not success:
                    logger.error("Failed to apply changes")
                    if self._backup_path:
                        logger.info("Restoring from backup...")
                        self.restore_from_backup()
                    return False

                # Prompt user for approval
                response = input("\nDo you want to keep these changes? (y/n): ").lower()
                if response != 'y':
                    logger.info("Changes rejected, restoring original file...")
                    if not self.restore_from_backup():
                        logger.error("Failed to restore from backup")
                        return False
                    return False

                # Changes approved - save current state
                self.workbook.save()
                logger.info("Changes saved successfully")
                
                # Create new backup of approved state
                if not self.create_backup():
                    logger.warning("Failed to create backup of approved changes")
                    return False
                logger.debug("Created backup of approved changes")
                
            else:
                logger.info("Dry run mode - changes validated but not applied:")
                for change in validated_changes:
                    logger.info(f"Would apply: {change.operation} to {change.target}")

            return True

        except Exception as e:
            logger.error(f"Error applying changes: {str(e)}")
            if self._backup_path:
                logger.info("Restoring from backup due to error...")
                self.restore_from_backup()
            return False

    def _apply_validated_changes(self, changes: List[ExcelChange]) -> bool:
        """Apply pre-validated changes to the worksheet"""
        try:
            for change in changes:
                if change.operation == OperationType.COPY:
                    source, target = change.target.split(" to ")
                    source_range = self.active_sheet.range(source)
                    target_range = self.active_sheet.range(target)
                    source_range.copy(target_range)
                else:
                    range_obj = self.active_sheet.range(change.target)
                    
                    if change.operation == OperationType.UPDATE:
                        range_obj.value = change.value
                    elif change.operation == OperationType.FORMULA:
                        range_obj.formula = change.value
                    elif change.operation == OperationType.FORMAT:
                        if change.value.get("bold"):
                            range_obj.font.bold = True
                    elif change.operation == OperationType.NUMBER_FORMAT:
                        if change.value == "currency":
                            range_obj.number_format = "$#,##0.00"
                    elif change.operation == OperationType.COLUMN_WIDTH:
                        range_obj.column_width = change.value
                    elif change.operation == OperationType.CLEAR:
                        range_obj.clear_contents()
                    elif change.operation == OperationType.INSERT_ROW:
                        row_num = int(change.target.split(':')[0])
                        self.active_sheet.api.Rows(row_num).Insert()
                    elif change.operation == OperationType.DELETE_COLUMN:
                        col_letter = change.target.split(':')[0]
                        self.active_sheet.api.Columns(col_letter).Delete()
                    elif change.operation == OperationType.NAMED_RANGE:
                        start, end = change.target.split(':')
                        start_col, start_row = self._parse_cell_reference(start)
                        end_col, end_row = self._parse_cell_reference(end)
                        range_ref = f"${start_col}${start_row}:${end_col}${end_row}"
                        self.workbook.names.add(
                            change.value,
                            f"=Sheet1!{range_ref}"
                        )
                
                change.status = "applied"
                self.change_history.append(change)
                
            return True
            
        except Exception as e:
            logger.error(f"Error applying validated changes: {str(e)}")
            return False

    def _create_new_model(self, instructions: Dict) -> bool:
        """Create a new Excel model based on instructions."""
        try:
            if not self.app and not self._initialize_excel():
                return False

            if not instructions.get('model_name'):
                raise ValueError("Model name not provided")
            
            if not self.workbook:
                self.workbook = self.app.books.add()
                self.active_sheet = self.workbook.sheets.active
            
            for sheet_info in instructions.get('sheets', []):
                # Add sheet if it doesn't exist
                sheet_name = sheet_info['name']
                try:
                    sheet = self.workbook.sheets[sheet_name]
                except:
                    sheet = self.workbook.sheets.add(sheet_name)
                
                # Apply structure
                for item in sheet_info.get('structure', []):
                    if 'formula' in item:
                        sheet.range(item['range']).formula = item['formula']
                    else:
                        sheet.range(item['range']).value = item.get('value') or item.get('values')
            
            # Save the workbook
            self.workbook.save(instructions['model_name'])
            return True
            
        except Exception as e:
            logger.error(f"Error creating new model: {str(e)}")
            if self.app:
                try:
                    self.app.quit()
                except:
                    pass
            return False

    def _convert_value(self, value: str) -> Union[float, int, str]:
        """Convert string value to appropriate type."""
        try:
            # Try converting to float first
            return float(value)
        except ValueError:
            # If not a number, return as string
            return value

    def save_and_close(self, save_path: Optional[str] = None) -> bool:
        """Save and close the workbook, but keep Excel running."""
        try:
            if self.workbook:
                if save_path:
                    self.workbook.save(save_path)
                else:
                    self.workbook.save()
                self.workbook.close()  # Only close the workbook
                self.workbook = None   # Clear the reference
                return True
            return False
        except Exception as e:
            logger.error(f"Error saving workbook: {str(e)}")
            return False

    def _parse_change_instruction(self, change: str) -> Optional[ExcelChange]:
        """Parse a change instruction into an ExcelChange object"""
        try:
            # Basic operations
            if "Update cell" in change:
                match = re.search(r"([A-Z]+[0-9]+)", change)
                if not match:
                    return None
                cell_ref = match.group(1)
                value = change.split(" to ")[-1]
                return ExcelChange(
                    operation=OperationType.UPDATE,
                    target=cell_ref,
                    value=self._convert_value(value)
                )
            
            elif "Format" in change and "as header" in change:
                range_ref = re.search(r"([A-Z]+[0-9]+:[A-Z]+[0-9]+)", change).group(1)
                return ExcelChange(
                    operation=OperationType.FORMAT,
                    target=range_ref,
                    value={"bold": True}
                )
            
            elif "Set" in change and "number format" in change:
                range_ref = re.search(r"([A-Z]+[0-9]+:[A-Z]+[0-9]+)", change).group(1)
                format_type = "currency" if "currency" in change else None
                return ExcelChange(
                    operation=OperationType.NUMBER_FORMAT,
                    target=range_ref,
                    value=format_type
                )
            
            elif "Set" in change and "formula" in change:
                # Match both single cell and range references
                range_pattern = r"([A-Z]+[0-9]+(?::[A-Z]+[0-9]+)?)"
                range_ref = re.search(f"Set {range_pattern} formula to", change).group(1)
                formula = change.split(" to ")[-1]
                return ExcelChange(
                    operation=OperationType.FORMULA,
                    target=range_ref,
                    value=formula
                )
            
            elif "Copy range" in change:
                # Example: "Copy range A1:A10 to B1"
                source_range = re.search(r"([A-Z]+[0-9]+:[A-Z]+[0-9]+)", change).group(1)
                target_cell = re.search(r"to ([A-Z]+[0-9]+)", change).group(1)
                return ExcelChange(
                    operation=OperationType.COPY,
                    target=f"{source_range} to {target_cell}",
                    value=None
                )
            
            elif "Set column" in change and "width" in change:
                column = re.search(r"column ([A-Z]+)", change).group(1)
                width = int(re.search(r"to (\d+)", change).group(1))
                return ExcelChange(
                    operation=OperationType.COLUMN_WIDTH,
                    target=f"{column}:{column}",
                    value=width
                )
            
            elif "Clear contents" in change:
                range_ref = re.search(r"([A-Z]+[0-9]+:[A-Z]+[0-9]+)", change).group(1)
                return ExcelChange(
                    operation=OperationType.CLEAR,
                    target=range_ref,
                    value=None
                )
            
            elif "Insert row" in change:
                position = re.search(r"position (\d+)", change).group(1)
                return ExcelChange(
                    operation=OperationType.INSERT_ROW,
                    target=f"{position}:{position}",
                    value=None
                )
            
            elif "Delete column" in change:
                column = re.search(r"column ([A-Z]+)", change).group(1)
                return ExcelChange(
                    operation=OperationType.DELETE_COLUMN,
                    target=f"{column}:{column}",
                    value=None
                )
            
            elif "Create named range" in change:
                # Improved pattern for named range
                match = re.search(r"range (\w+) for ([A-Z]+[0-9]+:[A-Z]+[0-9]+)", change)
                if not match:
                    raise ValueError(f"Invalid named range format: {change}")
                name, range_ref = match.groups()
                return ExcelChange(
                    operation=OperationType.NAMED_RANGE,
                    target=range_ref,
                    value=name
                )
            
            else:
                logger.warning(f"Unrecognized change instruction: {change}")
                return None
            
        except Exception as e:
            logger.error(f"Error parsing change instruction: {str(e)}")
            return None

    def restore_from_backup(self) -> bool:
        """Restore current file from backup"""
        try:
            if self._backup_path and os.path.exists(self._backup_path):
                current_file = os.path.abspath(self.workbook.fullname)
                backup_path = os.path.abspath(self._backup_path)
                
                # Close current workbook
                self.workbook.close()
                
                # Delete current file
                if os.path.exists(current_file):
                    os.remove(current_file)
                
                # Copy backup to current location
                import shutil
                shutil.copy2(backup_path, current_file)
                
                # Reopen the current file
                self.workbook = self.app.books.open(current_file)
                self.active_sheet = self.workbook.sheets.active
                self.workbook.activate()  # Ensure the restored file is visible
                
                logger.info("Restored from backup")
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to restore from backup: {str(e)}")
            return False 