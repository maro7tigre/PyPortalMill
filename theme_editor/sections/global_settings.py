"""
Global Settings Section
Colors, Typography, etc.
"""

from PySide6.QtWidgets import QLabel, QVBoxLayout, QGridLayout
from PySide6.QtCore import Qt
from ..base_section import ThemeEditorSection

class GlobalSection(ThemeEditorSection):
    def setup_config_ui(self):
        self.add_header("Background Colors")
        self.add_color_control("Primary", "backgrounds.primary", "#1d1f28")
        self.add_color_control("Secondary", "backgrounds.secondary", "#0d0f18")
        self.add_color_control("Tertiary", "backgrounds.tertiary", "#44475c")
        self.add_color_control("Input Fields", "backgrounds.input", "#1d1f28")
        
        self.add_header("Text Colors")
        self.add_color_control("Primary", "text.primary", "#ffffff")
        self.add_color_control("Secondary", "text.secondary", "#bdbdc0")
        self.add_color_control("Disabled", "text.disabled", "#6f779a")
        self.add_color_control("Links", "text.links", "#00c4fe")
        
        self.add_header("Accent Colors")
        self.add_color_control("Primary", "accents.primary", "#BB86FC")
        self.add_color_control("Success", "accents.secondary", "#23c87b")
        self.add_color_control("Warning", "accents.warning", "#ff8c00")
        self.add_color_control("Error", "accents.error", "#ff4a7c")
        
        self.add_header("Border Colors")
        self.add_color_control("Active", "borders.active", "#BB86FC")
        self.add_color_control("Inactive", "borders.inactive", "#6f779a")

    def setup_preview_ui(self):
        # Create a mini dashboard to show global colors
        grid = QGridLayout()
        grid.setSpacing(10)
        
        self.bg_preview = QLabel("Background Primary")
        self.bg_preview.setFixedSize(140, 80)
        self.bg_preview.setAlignment(Qt.AlignCenter)
        grid.addWidget(self.bg_preview, 0, 0)
        
        self.sec_preview = QLabel("Background Secondary")
        self.sec_preview.setFixedSize(140, 80)
        self.sec_preview.setAlignment(Qt.AlignCenter)
        grid.addWidget(self.sec_preview, 0, 1)
        
        self.accent_preview = QLabel("Accent Primary")
        self.accent_preview.setFixedSize(140, 40)
        self.accent_preview.setAlignment(Qt.AlignCenter)
        grid.addWidget(self.accent_preview, 1, 0)
        
        self.text_preview = QLabel("Primary Text")
        self.text_preview.setAlignment(Qt.AlignCenter)
        grid.addWidget(self.text_preview, 1, 1)
        
        self.preview_inner_layout.addLayout(grid)
        self.preview_inner_layout.addStretch()
        
    def update_preview(self):
        # Update styles based on current values
        bg_p = self.get_style_value("backgrounds.primary", "#000")
        bg_s = self.get_style_value("backgrounds.secondary", "#111")
        text_p = self.get_style_value("text.primary", "#fff")
        accent = self.get_style_value("accents.primary", "#f00")
        border = self.get_style_value("borders.active", "#ccc")
        
        self.bg_preview.setStyleSheet(f"background-color: {bg_p}; color: {text_p}; border: 1px solid {border};")
        self.sec_preview.setStyleSheet(f"background-color: {bg_s}; color: {text_p}; border: 1px dashed {border};")
        self.accent_preview.setStyleSheet(f"background-color: {accent}; color: #fff; border-radius: 4px;")
        self.text_preview.setStyleSheet(f"color: {text_p}; font-size: 14px;")
