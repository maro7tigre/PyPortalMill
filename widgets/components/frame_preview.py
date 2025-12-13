"""
Drawing Preview Widget

Visual preview area for custom drawings with theme-based background.
This is an empty drawing canvas that expands to fill available space.
"""

from PySide6.QtWidgets import QWidget, QSizePolicy, QStyle, QStyleOption
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter
from widgets.mixins import ThemedWidgetMixin
from core.theme_manager import get_theme_manager


class DrawingPreview(QWidget, ThemedWidgetMixin):
    """Empty visual preview area for custom drawings with theme integration"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        ThemedWidgetMixin.__init__(self)
        
        # Configuration storage (can be updated via update_config)
        self.config = {}
        
        # Set size policy to expand
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # Get minimum size from theme
        tm = get_theme_manager()
        min_width = tm.get_style('drawing_preview.min_width') or 400
        min_height = tm.get_style('drawing_preview.min_height') or 400
        self.setMinimumSize(int(min_width), int(min_height))
        
        self._apply_theme()
    
    def _apply_theme(self):
        """Apply theme colors and minimum dimensions"""
        tm = get_theme_manager()
        
        # Update minimum size from theme
        min_width = tm.get_style('drawing_preview.min_width') or 400
        min_height = tm.get_style('drawing_preview.min_height') or 400
        self.setMinimumSize(int(min_width), int(min_height))
        
        # Apply colors
        bg = tm.get_color('drawing_preview.background') or tm.get_color('backgrounds.secondary')
        border = tm.get_color('drawing_preview.border') or tm.get_color('borders.inactive')
        self.setStyleSheet(f"background-color: {bg}; border: 1px solid {border};")
        self.update()
    
    def update_config(self, config):
        """Update preview with new configuration"""
        self.config = config
        self.update()
    
    def paintEvent(self, event):
        """Paint event - override this to render custom drawings"""
        # First, draw the standard widget background/border from stylesheet
        opt = QStyleOption()
        opt.initFrom(self)
        painter = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, painter, self)
        
        # Enable antialiasing for any custom drawing
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Empty by default - users can subclass or connect to draw custom shapes
        # Users can override this method or set a custom paint function
        pass

