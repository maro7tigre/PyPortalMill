from PySide6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QLabel, QRadioButton, QButtonGroup, 
    QSpinBox, QCheckBox, QLineEdit, QWidget, QFrame
)
from PySide6.QtCore import Qt
from ..base_section import ThemeEditorSection

class VariablesSection(ThemeEditorSection):
    def setup_config_ui(self):
        self.add_header("Variable Layout")
        
        # Orientation
        self.config_layout.addWidget(QLabel("Label Position"))
        self.orientation_group = QButtonGroup(self)
        
        row_o = QWidget()
        lay_o = QHBoxLayout(row_o)
        
        rb_h = QRadioButton("Horizontal (Side-by-Side)")
        rb_v = QRadioButton("Vertical (Label on Top)")
        
        self.orientation_group.addButton(rb_h, 0)
        self.orientation_group.addButton(rb_v, 1)
        
        # Set initial
        current_orient = self.get_style_value("layouts.variables.orientation", "horizontal")
        if current_orient == "vertical":
            rb_v.setChecked(True)
        else:
            rb_h.setChecked(True)
            
        self.orientation_group.idClicked.connect(self._on_orientation_changed)
        
        lay_o.addWidget(rb_h)
        lay_o.addWidget(rb_v)
        lay_o.addStretch()
        self.config_layout.addWidget(row_o)
        
        # Spacing
        self.add_number_control("Spacing (Label <-> Input)", "layouts.variables.spacing", 8, 0, 50)
        
        self.add_header("Input Sizing")
        
        # Fixed vs Expand
        row_s = QWidget()
        lay_s = QHBoxLayout(row_s)
        
        self.cb_expand = QCheckBox("Expand to fill available space")
        is_expanded = self.get_style_value("layouts.variables.expand", True)
        self.cb_expand.setChecked(is_expanded)
        self.cb_expand.toggled.connect(lambda c: self.set_theme_value("layouts.variables.expand", c))
        
        lay_s.addWidget(self.cb_expand)
        self.config_layout.addWidget(row_s)
        
        # Fixed Width (if not expanded)
        self.add_number_control("Fixed Width", "layouts.variables.fixed_width", 150, 50, 500)
        
    def _on_orientation_changed(self, id):
        val = "vertical" if id == 1 else "horizontal"
        self.set_theme_value("layouts.variables.orientation", val)

    def setup_preview_ui(self):
        layout = self.preview_inner_layout
        
        layout.addWidget(QLabel("Preview:"))
        
        self.preview_container = QWidget()
        self.preview_container.setStyleSheet("background-color: #282a36; border-radius: 4px; padding: 10px;")
        layout.addWidget(self.preview_container)
        
        self.update_preview()
        layout.addStretch()

    def update_preview(self):
        # Rebuild preview based on current settings
        if hasattr(self, 'preview_container'):
            # Clear old layout
            if self.preview_container.layout():
                QWidget().setLayout(self.preview_container.layout()) # Ownership trick to delete layout
            
            # Get settings
            orientation = self.get_style_value("layouts.variables.orientation", "horizontal")
            spacing = int(self.get_style_value("layouts.variables.spacing", 8))
            expand = self.get_style_value("layouts.variables.expand", True)
            fixed_w = int(self.get_style_value("layouts.variables.fixed_width", 150))
            
            # Main Layout for container
            main_layout = QVBoxLayout(self.preview_container)
            
            # Create a mock variable row
            row = QWidget()
            if orientation == "vertical":
                l = QVBoxLayout(row)
            else:
                l = QHBoxLayout(row)
                
            l.setContentsMargins(0,0,0,0)
            l.setSpacing(spacing)
            
            label = QLabel("Variable Name:")
            label.setStyleSheet("color: #bdbdc0;")
            
            inp = QLineEdit("123.45")
            inp.setStyleSheet("padding: 4px; border-radius: 4px; border: 1px solid #666; background: #1d1f28; color: white;")
            
            if expand:
                if orientation == "horizontal":
                    l.addWidget(label)
                    l.addWidget(inp, 1) # Expand
                else:
                    l.addWidget(label)
                    l.addWidget(inp) # Vertical automatically expands width usually, or we set it
            else:
                inp.setFixedSize(fixed_w, 24)
                l.addWidget(label)
                l.addWidget(inp)
                if orientation == "horizontal":
                     l.addStretch()
                     
            main_layout.addWidget(row)
