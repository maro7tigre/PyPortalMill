"""
Inputs Section
Configuration for input fields (LineEdits, SpinBoxes, etc).
"""

from PySide6.QtWidgets import QCheckBox, QRadioButton
from ..base_section import ThemeEditorSection
from widgets.primitives.inputs import ThemedLineEdit, ThemedSpinBox, ThemedCheckBox, ThemedRadioButton, ErrorLineEdit

class InputsSection(ThemeEditorSection):
    def setup_config_ui(self):
        self.add_header("Dimensions & Borders")
        self.add_number_control("Border Radius (px)", "styles.inputs.border_radius", 4, 0, 30)
        self.add_number_control("Padding Horiz (px)", "styles.inputs.padding_horizontal", 12, 0, 50)
        self.add_number_control("Padding Vert (px)", "styles.inputs.padding_vertical", 6, 0, 30)
        self.add_number_control("Border Width (px)", "styles.inputs.border_width", 1, 0, 10)
        self.add_number_control("Focus Width (px)", "styles.inputs.focus_border_width", 2, 0, 10)
        self.add_number_control("Font Size (pt)", "styles.inputs.font_size", 10, 6, 30)
        
        self.add_header("Focus State")
        self.add_color_control("Focus Border Color", "borders.active", "#BB86FC")
        
        self.add_header("Error State")
        self.add_color_control("Error Border Color", "accents.error", "#ff4a7c")

    def setup_preview_ui(self):
        layout = self.preview_inner_layout
        
        layout.addWidget(ThemedLineEdit("Standard Input"))
        layout.addWidget(ThemedSpinBox())
        
        err = ErrorLineEdit("Error Input")
        cb = QCheckBox("Toggle Error")
        cb.toggled.connect(err.set_error)
        layout.addWidget(err)
        layout.addWidget(cb)
        
        layout.addWidget(ThemedCheckBox("Checkbox Option"))
        layout.addWidget(ThemedRadioButton("Radio Option"))
        
        layout.addStretch()
