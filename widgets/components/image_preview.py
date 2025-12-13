"""
Image Preview Widget

A theme-aware image preview area with configurable size, padding, and styling.
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QSizePolicy, QStyle, QStyleOption
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QPixmap
from widgets.mixins import ThemedWidgetMixin
from widgets.primitives.labels import ScaledPreviewLabel
from core.theme_manager import get_theme_manager


class ConfigurablePreviewLabel(ScaledPreviewLabel):
    """Subclass of ScaledPreviewLabel that uses specific image_preview theme properties"""
    
    def update_style(self):
        """Override to use specific image_preview theme colors"""
        tm = get_theme_manager()
        
        bg = tm.get_color('image_preview.preview_background') or tm.get_color('backgrounds.tertiary')
        border = tm.get_color('image_preview.preview_border') or tm.get_color('borders.inactive')
        text_color = tm.get_color('image_preview.text_color') or tm.get_color('text.secondary')
        
        # Get text size from control styles or default
        text_size = tm.get_style('image_preview.text_size') or 14
        
        self.setStyleSheet(f"""
            QLabel {{
                background-color: {bg};
                border: 2px solid {border};
                border-radius: 4px;
                color: {text_color};
                font-size: {text_size}px;
                padding: 0px; 
            }}
        """)


class ImagePreview(QWidget, ThemedWidgetMixin):
    """
    Widget for displaying image previews with configurable layout and styling.
    
    Structure:
    - Layout (QWidget): Has background, border, and padding
      - Inner Label (ConfigurablePreviewLabel): Has its own background, border, and text
    """
    
    def __init__(self, width=400, height=400, placeholder_text="No Image", parent=None):
        super().__init__(parent)
        ThemedWidgetMixin.__init__(self)
        
        self.default_width = width
        self.default_height = height
        
        # Set size policy to expand
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0) # Will be updated by theme
        
        # Inner preview label
        self.preview_label = ConfigurablePreviewLabel()
        self.preview_label.setAlignment(Qt.AlignCenter)
        self.preview_label.setText(placeholder_text)
        
        self.layout.addWidget(self.preview_label)
        
        self._apply_theme()
    
    def _apply_theme(self):
        """Apply theme colors, dimensions, and padding"""
        tm = get_theme_manager()
        
        # Update minimum size from theme (control_styles)
        min_width = tm.get_style('image_preview.min_width') or self.default_width
        min_height = tm.get_style('image_preview.min_height') or self.default_height
        
        self.setMinimumSize(int(min_width), int(min_height))
        
        # Update Padding
        padding = tm.get_style('image_preview.padding')
        if padding is None:
            padding = 10
        self.layout.setContentsMargins(int(padding), int(padding), int(padding), int(padding))
        
        # Layout container styling (background and border) handled in paintEvent via stylesheet
        bg = tm.get_color('image_preview.layout_background') or tm.get_color('backgrounds.secondary')
        border = tm.get_color('image_preview.layout_border') or tm.get_color('borders.inactive')
        
        self.setStyleSheet(f"""
            ImagePreview {{
                background-color: {bg};
                border: 1px solid {border};
            }}
        """)
        
        # Update inner label style
        self.preview_label.update_style()
    
    def paintEvent(self, event):
        """Paint the widget background and border"""
        opt = QStyleOption()
        opt.initFrom(self)
        painter = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, painter, self)
    
    def set_placeholder_text(self, text):
        """Update placeholder text"""
        self.preview_label.setText(text)
    
    def set_image(self, image_path_or_pixmap):
        """Set the image to display"""
        if isinstance(image_path_or_pixmap, str):
            pixmap = QPixmap(image_path_or_pixmap)
        elif isinstance(image_path_or_pixmap, QPixmap):
            pixmap = image_path_or_pixmap
        else:
            pixmap = None
        
        if pixmap and not pixmap.isNull():
            self.preview_label.setPixmap(pixmap)
        else:
            self.clear_image()
    
    def clear_image(self):
        """Clear the image and show placeholder text"""
        self.preview_label.setText(self.placeholder_text)
    
    def set_placeholder_text(self, text):
        """Update the placeholder text"""
        self.placeholder_text = text
        if not self.preview_label._pixmap or self.preview_label._pixmap.isNull():
            self.preview_label.setText(text)
    
    def get_placeholder_text(self):
        """Get the current placeholder text"""
        return self.placeholder_text
