"""
Helper module for macOS-specific Excel operations
"""

import os
import subprocess
from loguru import logger

def launch_excel_macos():
    """Ensure Excel is running on macOS"""
    try:
        apple_script = '''
        tell application "Microsoft Excel"
            if not running then
                launch
                delay 1
            end if
        end tell
        '''
        
        # Write AppleScript to temporary file
        script_path = "/tmp/launch_excel.scpt"
        with open(script_path, "w") as f:
            f.write(apple_script)
        
        # Execute AppleScript
        result = subprocess.run(
            ["osascript", script_path],
            capture_output=True,
            text=True
        )
        
        # Clean up
        os.remove(script_path)
        
        return result.returncode == 0
            
    except Exception as e:
        logger.error(f"Error ensuring Excel is running: {str(e)}")
        return False 