# Mac Helper Module

## Overview
The Mac helper module provides macOS-specific functionality for system integration and automation.

## Components

### MacHelper Class
```python
class MacHelper:
    def __init__(self):
        """Initialize Mac helper utilities"""
    
    def activate_excel(self):
        """Bring Excel application to front"""
    
    def get_active_window(self) -> str:
        """Get currently active window information"""
    
    def set_clipboard(self, text: str):
        """Copy text to system clipboard"""
    
    def get_clipboard(self) -> str:
        """Get text from system clipboard"""
    
    def show_notification(self, title: str, message: str):
        """Show system notification"""
```

### System Integration
- Application activation
- Window management
- Clipboard operations
- System notifications 