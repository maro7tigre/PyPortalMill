"""
Base Section for Theme Editor
Defines the interface for all configuration sections.
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QScrollArea, 
                               QFrame, QGroupBox, QFormLayout, QGridLayout,
                               QLabel, QPushButton, QColorDialog, QSpinBox, 
                               QAbstractSpinBox)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor

class ThemeEditorSection(QWidget):
    """
    Abstract base class for a theme editor section.
    
    Layout:
    [ Configuration (Scrollable) ] | [ Preview (Fixed/Scrollable) ]
    """
    
    # Internal signal when any value changes (for auto-preview)
    data_changed = Signal()
    
    def __init__(self, parent_dialog):
        super().__init__()
        self.parent_dialog = parent_dialog
        self._inputs = {}  # Store input widgets by key
        self._previews = {} # Store preview widgets by key
        
        self._setup_main_layout()
        
    def _setup_main_layout(self):
        """Setup the split layout"""
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # --- LEFT: Configuration ---
        config_container = QWidget()
        self.config_layout = QVBoxLayout(config_container)
        self.config_layout.setContentsMargins(10, 10, 10, 10)
        self.config_layout.setAlignment(Qt.AlignTop)
        
        # Scroll area for config
        config_scroll = QScrollArea()
        config_scroll.setWidgetResizable(True)
        config_scroll.setWidget(config_container)
        config_scroll.setFrameShape(QFrame.NoFrame)
        
        # --- RIGHT: Preview ---
        preview_container = QWidget()
        self.preview_layout = QVBoxLayout(preview_container)
        self.preview_layout.setContentsMargins(20, 20, 20, 20)
        self.preview_layout.setAlignment(Qt.AlignTop)
        
        # Add a title to preview
        preview_title = QLabel("Live Preview")
        preview_title.setStyleSheet("font-weight: bold; font-size: 14px; color: #888; margin-bottom: 10px;")
        self.preview_layout.addWidget(preview_title)
        
        # Preview Area (Darker background to pop)
        self.preview_area = QFrame()
        self.preview_area.setObjectName("PreviewArea")
        self.preview_area.setStyleSheet("#PreviewArea { background-color: rgba(0,0,0,0.2); border-radius: 8px; }")
        self.preview_inner_layout = QVBoxLayout(self.preview_area)
        self.preview_inner_layout.setAlignment(Qt.AlignTop)
        
        self.preview_layout.addWidget(self.preview_area)
        self.preview_layout.addStretch()
        
        # Add to main splitter-like layout
        # We use simple layout with stretch factors for now: 40% Config, 60% Preview
        main_layout.addWidget(config_scroll, 4)
        
        # Vertical Separator
        sep = QFrame()
        sep.setFrameShape(QFrame.VLine)
        sep.setFrameShadow(QFrame.Sunken)
        sep.setStyleSheet("background-color: #444;")
        main_layout.addWidget(sep)
        
        main_layout.addWidget(preview_container, 6)
        
        # Call subclass setups
        self.setup_config_ui()
        self.setup_preview_ui()
        
        # Initial update
        self.update_preview()

    def setup_config_ui(self):
        """Override to add widgets to self.config_layout"""
        raise NotImplementedError

    def setup_preview_ui(self):
        """Override to add widgets to self.preview_inner_layout"""
        raise NotImplementedError
        
    def update_preview(self):
        """Override to update preview widgets based on current inputs"""
        pass

    # --- Helper Data Methods ---
    
    def get_theme_data(self):
        """Get the full theme data dictionary"""
        return self.parent_dialog.get_theme_data()
        
    def get_style_value(self, path, default=None):
        """Get a value from the theme dict using dot notation (e.g. 'buttons.radius')"""
        data = self.get_theme_data()
        
        # Handle control_styles separation if needed, 
        # normally inputs are in 'control_styles' and colors in root
        # We'll assume path is absolute from theme root for flexibility
        # But if it starts with 'styles.', we look in control_styles
        
        if path.startswith('styles.'):
            path = 'control_styles.' + path[7:]
            
        parts = path.split('.')
        value = data
        for part in parts:
            if isinstance(value, dict) and part in value:
                value = value[part]
            else:
                return default
        return value

    def set_theme_value(self, path, value):
        """Set a value in the theme dict using dot notation"""
        data = self.get_theme_data()
        
        if path.startswith('styles.'):
            path = 'control_styles.' + path[7:]
            
        parts = path.split('.')
        current = data
        for part in parts[:-1]:
            if part not in current:
                current[part] = {}
            current = current[part]
        current[parts[-1]] = value
        
        # Notify change
        self.data_changed.emit()
        self.update_preview()
        self.parent_dialog.apply_temporary_theme()

    # --- Helper Widget Builders ---

    def add_color_control(self, label, path, default="#000000"):
        """Add a color picker row"""
        row_widget = QWidget()
        layout = QHBoxLayout(row_widget)
        layout.setContentsMargins(0, 5, 0, 5)
        
        lbl = QLabel(label)
        layout.addWidget(lbl)
        layout.addStretch()
        
        btn = QPushButton()
        btn.setFixedSize(60, 25)
        
        current_val = self.get_style_value(path, default)
        btn.setStyleSheet(f"background-color: {current_val}; border: 1px solid #666;")
        
        btn.clicked.connect(lambda: self._pick_color(path, btn))
        
        # Store for referencing
        self._inputs[path] = btn
        
        layout.addWidget(btn)
        self.config_layout.addWidget(row_widget)
        return btn

    def add_number_control(self, label, path, default=0, min_val=0, max_val=100, step=1):
        """Add a number spinbox row"""
        row_widget = QWidget()
        layout = QHBoxLayout(row_widget)
        layout.setContentsMargins(0, 5, 0, 5)
        
        lbl = QLabel(label)
        layout.addWidget(lbl)
        layout.addStretch()
        
        spin = QSpinBox()
        spin.setRange(min_val, max_val)
        spin.setSingleStep(step)
        spin.setValue(int(self.get_style_value(path, default)))
        spin.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        spin.setFixedWidth(80)
        
        spin.valueChanged.connect(lambda v: self.set_theme_value(path, v))
        
        self._inputs[path] = spin
        
        layout.addWidget(spin)
        self.config_layout.addWidget(row_widget)
        return spin
        
    def add_header(self, title):
        """Add a section header"""
        lbl = QLabel(title)
        lbl.setStyleSheet("font-weight: bold; margin-top: 20px; margin-bottom: 5px; color: #BB86FC;")
        self.config_layout.addWidget(lbl)

    def _pick_color(self, path, btn):
        """Handle color picker"""
        current_hex = self.get_style_value(path, "#000000")
        color = QColorDialog.getColor(QColor(current_hex), self, "Select Color")
        
        if color.isValid():
            new_hex = color.name()
            btn.setStyleSheet(f"background-color: {new_hex}; border: 1px solid #666;")
            self.set_theme_value(path, new_hex)
