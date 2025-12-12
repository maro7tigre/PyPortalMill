from PySide6.QtWidgets import QWidget
from core.theme_manager import get_theme_manager

class ThemedWidgetMixin:
    """Mixin to handle dynamic theme updates"""
    
    def __init__(self):
        # Connect to theme change signal if specific updates are needed
        # Most widgets should receive updates via global stylesheet, 
        # but this allows for custom painting or non-stylesheet properties
        get_theme_manager().theme_changed.connect(self.on_theme_changed)
        
    def on_theme_changed(self, theme_name):
        """Override to handle custom theme updates"""
        pass
