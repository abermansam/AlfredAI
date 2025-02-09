"""
Main entry point for AlfredAI
"""

from excel_automation import ExcelHandler
from loguru import logger
import os
import platform
import time
from datetime import datetime

def check_excel_installation():
    """Check if Excel is properly installed and accessible"""
    try:
        if platform.system() == 'Darwin':  # macOS
            excel_path = '/Applications/Microsoft Excel.app'
            if not os.path.exists(excel_path):
                logger.error("Microsoft Excel not found. Please install Excel first.")
                return False
            logger.info("Excel installation found at: " + excel_path)
        return True
    except Exception as e:
        logger.error(f"Error checking Excel installation: {str(e)}")
        return False

def setup_directories():
    """Create necessary directories for output files"""
    output_dir = os.path.abspath("output")
    backup_dir = os.path.abspath(os.path.join(output_dir, "backups"))
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(backup_dir, exist_ok=True)
    return output_dir, backup_dir

def wait_for_user(message: str = "Press Enter to continue..."):
    """Wait for user input before continuing"""
    input(f"\n{message}")

def demo_excel_operations():
    """Demonstrate all Excel operations"""
    output_dir, backup_dir = setup_directories()
    handler = ExcelHandler(dry_run=True, visible=True)  # Start in dry run mode
    
    try:
        # Create/open workbook
        workbook_path = os.path.join(output_dir, "demo_workbook.xlsx")
        logger.info("Starting Excel operations demo...")
        
        if not handler._initialize_excel():
            logger.error("Failed to initialize Excel")
            return
        
        if not handler.open_workbook(workbook_path):
            logger.error("Failed to create workbook")
            return

        # Define all operations
        operations = [
            {
                'description': "Initial Setup",
                'changes': {
                    'required_changes': [
                        "Update cell A1 to Revenue Projections",
                        "Update cell A2 to 100",
                        "Update cell A3 to 200",
                        "Update cell A4 to 300",
                        "Update cell A5 to 400",
                        "Update cell B1 to Growth",
                        "Set B2:B5 formula to =A2*1.1"
                    ]
                }
            },
            {
                'description': "Format Worksheet",
                'changes': {
                    'required_changes': [
                        "Format A1:B1 as header with bold text",
                        "Set A2:A5 number format to currency",
                        "Set column A width to 15"
                    ]
                }
            },
            {
                'description': "Add Calculations",
                'changes': {
                    'required_changes': [
                        "Create named range BaseRevenue for A2:A5",
                        "Set B2:B5 formula to =SUM(A2:A5)*1.1",
                        "Set C1 formula to =AVERAGE(A2:A5)"
                    ]
                }
            }
        ]
        
        # Preview all operations first
        logger.info("\n=== Proposed Operations ===")
        for op in operations:
            logger.info(f"\n{op['description']}:")
            for change in op['changes']['required_changes']:
                logger.info(f"- {change}")
        
        # Ask to proceed with actual changes
        response = input("\nWould you like to proceed with these operations? (y/n): ").lower()
        if response != 'y':
            logger.info("Demo cancelled.")
            return

        # Switch to actual execution mode
        handler.dry_run = False
        
        # Execute each operation set
        for op in operations:
            logger.info(f"\n=== Executing {op['description']} ===")
            if not handler.apply_changes(op['changes']):
                logger.error(f"{op['description']} failed, moving to next operation...")
                continue
            
            logger.info(f"{op['description']} completed successfully!")
            wait_for_user("Review the changes before continuing...")

        logger.info("\nDemo completed!")
        wait_for_user("Press Enter to close Excel...")
            
    except Exception as e:
        logger.error(f"Error in demo: {str(e)}")
    finally:
        # Cleanup
        handler.cleanup()
        try:
            # Remove demo files
            if os.path.exists(workbook_path):
                os.remove(workbook_path)
            # Remove backup directory and contents
            if os.path.exists(backup_dir):
                import shutil
                shutil.rmtree(backup_dir)
            # Remove output directory if empty
            if os.path.exists(output_dir) and not os.listdir(output_dir):
                os.rmdir(output_dir)
        except Exception as e:
            logger.error(f"Error during cleanup: {str(e)}")

if __name__ == "__main__":
    logger.info("Starting Excel Operations Demo")
    demo_excel_operations() 