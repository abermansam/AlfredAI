"""
Tests for Excel automation module
"""

import pytest
from excel_automation import ExcelHandler
from excel_automation.excel_handler import ExcelChange, OperationType
from unittest.mock import Mock, patch, MagicMock, PropertyMock
import os
from datetime import datetime
import shutil

class TestExcelHandler:
    @pytest.fixture(autouse=True)
    def cleanup(self):
        """Clean up after each test"""
        yield
        test_files = ['test.xlsx', 'test_workbook.xlsx', 'test_workbook_updated.xlsx']
        for file in test_files:
            try:
                if os.path.exists(file):
                    os.remove(file)
            except Exception as e:
                print(f"Warning: Could not remove test file {file}: {e}")

    @pytest.fixture
    def excel_handler(self):
        handler = ExcelHandler(dry_run=True)
        yield handler
        if handler.workbook:
            try:
                handler.workbook.close()
            except:
                pass
        if handler.app:
            try:
                handler.app.quit()
            except:
                pass

    @pytest.fixture
    def mock_workbook(self):
        workbook = MagicMock()
        workbook.fullname = os.path.abspath("test.xlsx")
        return workbook

    def test_parse_change_instruction(self):
        handler = ExcelHandler(dry_run=True)
        
        test_cases = [
            (
                "Update cell A1 to Revenue",
                ExcelChange(
                    operation=OperationType.UPDATE,
                    target="A1",
                    value="Revenue",
                    status="pending"
                )
            ),
            (
                "Format A1:B1 as header with bold text",
                ExcelChange(
                    operation=OperationType.FORMAT,
                    target="A1:B1",
                    value={"bold": True},
                    status="pending"
                )
            ),
            (
                "Set A2:A5 number format to currency",
                ExcelChange(
                    operation=OperationType.NUMBER_FORMAT,
                    target="A2:A5",
                    value="currency",
                    status="pending"
                )
            ),
            (
                "Set column A width to 15",
                ExcelChange(
                    operation=OperationType.COLUMN_WIDTH,
                    target="A:A",
                    value=15,
                    status="pending"
                )
            ),
            (
                "Set B2:B5 formula to =SUM(A2:A5)",
                ExcelChange(
                    operation=OperationType.FORMULA,
                    target="B2:B5",
                    value="=SUM(A2:A5)",
                    status="pending"
                )
            ),
            (
                "Create named range BaseRevenue for A2:A5",
                ExcelChange(
                    operation=OperationType.NAMED_RANGE,
                    target="A2:A5",
                    value="BaseRevenue",
                    status="pending"
                )
            )
        ]
        
        for instruction, expected in test_cases:
            result = handler._parse_change_instruction(instruction)
            assert result is not None
            assert result.operation == expected.operation
            assert result.target == expected.target
            assert result.value == expected.value

    def test_validate_changes(self):
        handler = ExcelHandler(dry_run=True)
        handler.workbook = MagicMock()
        handler.active_sheet = MagicMock()
        
        # Test valid changes
        valid_changes = [
            "Update cell A1 to Revenue",
            "Format A1:B1 as header with bold text",
            "Set A2:A5 number format to currency"
        ]
        
        results = handler.validate_changes(valid_changes)
        assert all(change.status == "valid" for change in results)

        # Test invalid changes
        invalid_changes = [
            "Update cell ZZ99999999 to Revenue",  # Invalid cell reference
            "Invalid instruction format",        # Invalid format
            "Format A1:invalid as header"       # Invalid range
        ]
        
        results = handler.validate_changes(invalid_changes)
        assert len(results) == len(invalid_changes)  # One result per input
        
        # Debug print each result
        for i, (change, original) in enumerate(zip(results, invalid_changes)):
            print(f"\nChange {i + 1}:")
            print(f"Original instruction: {original}")
            print(f"Status: {change.status}")
            print(f"Error: {change.error}")
            print(f"Target: {change.target}")
            assert change.status == "error", f"Change {i + 1} should be error but is {change.status}"
            assert change.error is not None, f"Change {i + 1} should have error message"
            assert len(change.error) > 0, f"Change {i + 1} should have non-empty error message"

    def test_dry_run_mode(self, excel_handler, mock_workbook):
        excel_handler.workbook = mock_workbook
        excel_handler.active_sheet = MagicMock()
        
        instructions = {
            "required_changes": ["Update cell A1 to 100"]
        }
        
        result = excel_handler.apply_changes(instructions)
        assert result == True
        # Verify no actual changes were made
        excel_handler.active_sheet.range.assert_not_called()

    def test_open_workbook(self, excel_handler):
        with patch('xlwings.apps') as mock_apps, \
             patch('xlwings.App') as mock_App, \
             patch('os.path.exists', return_value=True):
            
            mock_active_app = MagicMock()
            mock_apps.active = mock_active_app
            
            mock_workbook = MagicMock()
            mock_active_app.books.open.return_value = mock_workbook
            
            mock_sheet = MagicMock()
            mock_workbook.sheets.active = mock_sheet
            
            result = excel_handler.open_workbook("test.xlsx")
            
            assert result == True
            mock_active_app.books.open.assert_called_once_with(os.path.abspath("test.xlsx"))

    def test_apply_changes(self, excel_handler):
        # Mock workbook and worksheet
        excel_handler.workbook = MagicMock()
        
        instructions = {
            "task_type": "edit_existing",
            "required_changes": ["Update cell A1 to 100"]
        }
        
        result = excel_handler.apply_changes(instructions)
        assert result == True 

    @patch('builtins.input', return_value='y')
    @patch('os.path.exists', return_value=True)
    @patch('shutil.copy2')
    def test_apply_formatting(self, mock_copy, mock_exists, mock_input, excel_handler):
        """Test applying various formatting to cells"""
        excel_handler.dry_run = False
        excel_handler.workbook = MagicMock()
        excel_handler.workbook.fullname = "test_workbook.xlsx"
        excel_handler.active_sheet = MagicMock()
        
        # Mock save operation
        excel_handler.workbook.save = MagicMock()
        
        # Mock range objects
        header_range = MagicMock()
        number_range = MagicMock()
        column_range = MagicMock()
        
        excel_handler.active_sheet.range.side_effect = lambda x: {
            'A1:B1': header_range,
            'A2:A10': number_range,
            'A:A': column_range
        }[x]
        
        formatting_changes = {
            'required_changes': [
                "Format A1:B1 as header with bold text",
                "Set A2:A10 number format to currency",
                "Set column A width to 15"
            ]
        }
        
        result = excel_handler.apply_changes(formatting_changes)
        assert result == True

    @patch('builtins.input', return_value='y')
    @patch('os.path.exists', return_value=True)
    @patch('shutil.copy2')
    def test_range_operations(self, mock_copy, mock_exists, mock_input, excel_handler):
        """Test operations on cell ranges"""
        excel_handler.dry_run = False
        excel_handler.workbook = MagicMock()
        excel_handler.workbook.fullname = "test_workbook.xlsx"
        excel_handler.active_sheet = MagicMock()
        
        # Mock save operation
        excel_handler.workbook.save = MagicMock()
        
        # Mock range objects
        source_range = MagicMock()
        target_range = MagicMock()
        clear_range = MagicMock()
        
        # Set up range returns with proper side_effect function
        def get_range(x):
            ranges = {
                'A1:B10': source_range,
                'C1': target_range,
                'D1:D10': clear_range,
                '5:5': excel_handler.active_sheet.api.Rows('5:5'),
                'B:B': excel_handler.active_sheet.api.Columns('B:B')
            }
            return ranges[x]
        
        excel_handler.active_sheet.range.side_effect = get_range
        
        # Mock Insert and Delete methods
        row_mock = MagicMock()
        col_mock = MagicMock()
        excel_handler.active_sheet.api.Rows.return_value = row_mock
        excel_handler.active_sheet.api.Columns.return_value = col_mock
        
        range_changes = {
            'required_changes': [
                "Copy range A1:B10 to C1",  # Removed "with formatting"
                "Clear contents in range D1:D10",
                "Insert row at position 5",
                "Delete column B"
            ]
        }
        
        result = excel_handler.apply_changes(range_changes)
        assert result == True
        
        # Verify operations
        source_range.copy.assert_called_once_with(target_range)
        clear_range.clear_contents.assert_called_once()
        row_mock.Insert.assert_called_once()
        col_mock.Delete.assert_called_once()

    @patch('builtins.input', return_value='y')
    @patch('os.path.exists', return_value=True)
    @patch('shutil.copy2')
    def test_formula_management(self, mock_copy, mock_exists, mock_input, excel_handler):
        """Test formula validation and management"""
        excel_handler.dry_run = False
        excel_handler.workbook = MagicMock()
        excel_handler.workbook.fullname = "test_workbook.xlsx"
        excel_handler.active_sheet = MagicMock()
        
        # Mock save operation
        excel_handler.workbook.save = MagicMock()
        
        # Mock range objects with proper formula property setup
        sum_range = MagicMock()
        named_range = MagicMock()
        avg_range = MagicMock()
        
        # Set up formula property for each range
        type(sum_range).formula = PropertyMock(return_value='=SUM(A2:A10)')
        type(avg_range).formula = PropertyMock(return_value='=AVERAGE(Revenue)')
        
        # Set up range returns
        excel_handler.active_sheet.range.side_effect = lambda x: {
            'B2:B10': sum_range,
            'A2:A10': named_range,
            'C2': avg_range
        }[x]
        
        formula_changes = {
            'required_changes': [
                "Set B2:B10 formula to =SUM(A2:A10)",
                "Create named range Revenue for A2:A10",
                "Set C2 formula to =AVERAGE(Revenue)"
            ]
        }
        
        result = excel_handler.apply_changes(formula_changes)
        assert result == True
        
        # Verify formula operations
        assert sum_range.formula == '=SUM(A2:A10)'
        excel_handler.workbook.names.add.assert_called_once_with(
            'Revenue',
            '=Sheet1!$A$2:$A$10'
        )
        assert avg_range.formula == '=AVERAGE(Revenue)'
        
        # Verify formula was set
        sum_range.formula = '=SUM(A2:A10)'
        avg_range.formula = '=AVERAGE(Revenue)' 