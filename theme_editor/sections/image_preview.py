"""
Image Preview Section for Theme Editor
"""

from PySide6.QtWidgets import QLabel, QLineEdit, QFormLayout, QWidget
from PySide6.QtCore import Qt
from ..base_section import ThemeEditorSection
from widgets.components.image_preview import ImagePreview


class ImagePreviewSection(ThemeEditorSection):
    def setup_config_ui(self):
        """Setup configuration controls"""
        self.add_header("Layout Appearance")
        self.add_color_control("Layout Background", "image_preview.layout_background", "#1d1f28")
        self.add_color_control("Layout Border", "image_preview.layout_border", "#6f779a")
        self.add_number_control("Padding (px)", "styles.image_preview.padding", 10, 0, 100)
        
        self.add_header("Preview Appearance")
        self.add_color_control("Preview Background", "image_preview.preview_background", "#0d0f18")
        self.add_color_control("Preview Border", "image_preview.preview_border", "#44475c")
        self.add_color_control("Text Color", "image_preview.text_color", "#8b95c0")
        self.add_number_control("Text Size (px)", "styles.image_preview.text_size", 14, 8, 72)
        
        self.add_header("Minimum Dimensions")
        self.add_number_control("Min Width (px)", "styles.image_preview.min_width", 400, 100, 2000, 10)
        self.add_number_control("Min Height (px)", "styles.image_preview.min_height", 400, 100, 2000, 10)
        
        # Placeholder text
        self.add_header("Content")
        
        # Add text input for placeholder
        row_widget = QWidget()
        layout = QFormLayout(row_widget)
        layout.setContentsMargins(0, 5, 0, 5)
        
        self.placeholder_input = QLineEdit()
        self.placeholder_input.setText(self.get_style_value("image_preview.placeholder_text", "No Image"))
        self.placeholder_input.textChanged.connect(self._on_placeholder_changed)
        
        layout.addRow("Placeholder Text:", self.placeholder_input)
        self.config_layout.addWidget(row_widget)
        
        self.config_layout.addStretch()
    
    def _on_placeholder_changed(self, text):
        """Handle placeholder text change"""
        self.set_theme_value("image_preview.placeholder_text", text)
        if hasattr(self, 'preview_widget'):
            self.preview_widget.set_placeholder_text(text)
    
    def setup_preview_ui(self):
        """Setup preview widgets"""
        layout = self.preview_inner_layout
        
        # Reset alignment to allow expansion
        layout.setAlignment(Qt.Alignment())
        
        # Make the preview area expand (remove spacer if exists)
        if hasattr(self, 'preview_layout') and hasattr(self, 'preview_area'):
             self.preview_layout.setStretchFactor(self.preview_area, 1)
             
             count = self.preview_layout.count()
             if count > 2:
                 item = self.preview_layout.itemAt(count - 1)
                 if item.spacerItem(): 
                     self.preview_layout.takeAt(count - 1)
        
        # Create preview widget
        placeholder_text = self.get_style_value("image_preview.placeholder_text", "No Image")
        # Ensure text is string, get_style_value might return None theoretically but default provided
        if not isinstance(placeholder_text, str):
            placeholder_text = str(placeholder_text)
            
        self.preview_widget = ImagePreview(
            placeholder_text=placeholder_text
        )
        
        layout.addWidget(self.preview_widget)
        # widget expands automatically due to expanding size policy
    
    def update_preview(self):
        """Update preview when theme changes"""
        if hasattr(self, 'preview_widget'):
            self.preview_widget._apply_theme()
