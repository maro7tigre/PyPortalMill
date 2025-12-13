"""
Drawing Preview Section for Theme Editor
"""

from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt
from ..base_section import ThemeEditorSection
from widgets.components.frame_preview import DrawingPreview


class DrawingPreviewSection(ThemeEditorSection):
    def setup_config_ui(self):
        """Setup configuration controls"""
        self.add_header("Canvas Appearance")
        
        # Background and border
        self.add_color_control("Background", "drawing_preview.background", "#0d0f18")
        self.add_color_control("Border", "drawing_preview.border", "#6f779a")
        
        # Minimum dimensions
        self.add_header("Minimum Dimensions")
        self.add_number_control("Min Width (px)", "styles.drawing_preview.min_width", 400, 100, 2000, 10)
        self.add_number_control("Min Height (px)", "styles.drawing_preview.min_height", 400, 100, 2000, 10)
        
        self.config_layout.addStretch()
    
    def setup_preview_ui(self):
        """Setup preview widgets"""
        layout = self.preview_inner_layout
        
        # Reset alignment to allow expansion (base class sets AlignTop)
        layout.setAlignment(Qt.Alignment())
        
        # Make the preview area expand in the parent layout
        # (base class adds a stretch at the bottom which we need to remove or overcome)
        if hasattr(self, 'preview_layout') and hasattr(self, 'preview_area'):
             # Try to remove the stretch item added by base class (it's usually the last item)
             # Layout has: Title, PreviewArea, Stretch. So index 2.
             # But safer to just set high stretch on our area and maybe remove the spacer if possible.
             # Let's set stretch factor to 1 on the preview area.
             self.preview_layout.setStretchFactor(self.preview_area, 1)
             
             # Also try to remove the spacer at the end to be sure
             count = self.preview_layout.count()
             if count > 2:
                 item = self.preview_layout.itemAt(count - 1)
                 if item.spacerItem(): # It's a spacer
                     self.preview_layout.takeAt(count - 1)

        # Create empty preview widget that expands (no label)
        self.preview_widget = DrawingPreview()
        
        layout.addWidget(self.preview_widget)
        # No stretch - let the widget expand to fill all available space
    
    def update_preview(self):
        """Update preview when theme changes"""
        if hasattr(self, 'preview_widget'):
            self.preview_widget._apply_theme()
