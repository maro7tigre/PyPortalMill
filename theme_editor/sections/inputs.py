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
        
        self.add_header("Normal State")
        self.add_color_control("Background", "inputs.normal.background", "#1e1e1e")
        self.add_color_control("Border", "inputs.normal.border", "#3e3e42")
        self.add_color_control("Text", "inputs.normal.text", "#ffffff")
        
        self.add_header("Focus State")
        self.add_color_control("Background", "inputs.focused.background", "#1e1e1e")
        self.add_color_control("Border", "inputs.focused.border", "#0078d4")
        self.add_color_control("Text", "inputs.focused.text", "#ffffff")
        
        self.add_header("Error State")
        self.add_color_control("Background", "inputs.error.background", "#1e1e1e")
        self.add_color_control("Border", "inputs.error.border", "#f44336")
        self.add_color_control("Text", "inputs.error.text", "#ffffff")

        self.add_header("Disabled State")
        self.add_color_control("Background", "inputs.disabled.background", "#1e1e1e")
        self.add_color_control("Border", "inputs.disabled.border", "#3e3e42")
        self.add_color_control("Text", "inputs.disabled.text", "#858585")

    def setup_preview_ui(self):
        layout = self.preview_inner_layout
        
        layout.addWidget(ThemedLineEdit("Standard Input"))
        layout.addWidget(ThemedSpinBox())
        
        err = ErrorLineEdit("Error Input")
        cb_err = QCheckBox("Toggle Error")
        cb_err.toggled.connect(err.set_error)
        
        dis_input = ThemedLineEdit("Disabled Input")
        cb_dis = QCheckBox("Toggle Disabled")
        cb_dis.toggled.connect(lambda c: dis_input.setDisabled(c))
        
        layout.addWidget(err)
        layout.addWidget(cb_err)
        layout.addWidget(dis_input)
        layout.addWidget(cb_dis)
        
        layout.addWidget(ThemedCheckBox("Checkbox Option"))
        layout.addWidget(ThemedRadioButton("Radio Option"))
        
        layout.addStretch()
