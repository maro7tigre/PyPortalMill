"""
Containers Section
Configuration for container widgets (GroupBoxes, ScrollAreas, etc).
"""

from ..base_section import ThemeEditorSection
from widgets.primitives.containers import ThemedGroupBox
from widgets.primitives.labels import ThemedLabel
from widgets.primitives.inputs import ThemedLineEdit

class ContainersSection(ThemeEditorSection):
    def setup_config_ui(self):
        self.add_header("GroupBox Style")
        self.add_number_control("Border Width (px)", "styles.groupbox.border_width", 1, 0, 10)
        self.add_number_control("Border Radius (px)", "styles.groupbox.border_radius", 4, 0, 20)
        self.add_number_control("Title Font Size (pt)", "styles.groupbox.title_font_size", 11, 8, 20)
        self.add_number_control("Padding (px)", "styles.groupbox.padding", 10, 0, 30)
        
        self.add_header("GroupBox Colors")
        self.add_color_control("Background", "groupbox.background", "#282a36")
        self.add_color_control("Border", "groupbox.border", "#6f779a")
        self.add_color_control("Title Text", "groupbox.title_color", "#ffffff")

    def setup_preview_ui(self):
        layout = self.preview_inner_layout
        
        # Preview GroupBox
        group1 = ThemedGroupBox("Standard GroupBox")
        from PySide6.QtWidgets import QVBoxLayout
        gl = QVBoxLayout(group1)
        gl.addWidget(ThemedLabel("Label inside group"))
        gl.addWidget(ThemedLineEdit("Input inside group"))
        layout.addWidget(group1)
        
        group2 = ThemedGroupBox("Another Section")
        gl2 = QVBoxLayout(group2)
        gl2.addWidget(ThemedLabel("More content"))
        layout.addWidget(group2)

        layout.addStretch()
