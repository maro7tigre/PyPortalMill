"""
Parameter Widget Factory
Creates UI widgets based on parameter configuration.
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                               QDoubleSpinBox, QComboBox, QCheckBox, QGroupBox, QSpinBox)
from PySide6.QtCore import Qt, Signal
from core.config_manager import ParameterConfig, ParameterSectionConfig, GroupedAutoConfig
from typing import Dict, Any, List

class ParameterWidget(QWidget):
    """Base class for parameter widgets"""
    value_changed = Signal(str, object) # param_name, new_value
    
    def __init__(self, config: ParameterConfig, parent=None):
        super().__init__(parent)
        self.config = config
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(2)
        
        self.setup_ui()
        
    def setup_ui(self):
        # Label with optional Auto checkbox if single auto
        header_layout = QHBoxLayout()
        self.label = QLabel(self.config.label)
        header_layout.addWidget(self.label)
        
        if self.config.has_auto:
            self.auto_cb = QCheckBox("Auto")
            self.auto_cb.stateChanged.connect(self._on_auto_toggled)
            header_layout.addWidget(self.auto_cb)
            
        header_layout.addStretch()
        self.layout.addLayout(header_layout)
        
        # Input Widget
        self.input_widget = self._create_input_widget()
        self.layout.addWidget(self.input_widget)
        
    def _create_input_widget(self):
        if self.config.type == "float":
            w = QDoubleSpinBox()
            w.setRange(self.config.min_value or 0, self.config.max_value or 99999)
            w.setValue(float(self.config.default))
            w.valueChanged.connect(lambda v: self.value_changed.emit(self.config.name, v))
            return w
        elif self.config.type == "int":
            w = QSpinBox()
            w.setRange(int(self.config.min_value or 0), int(self.config.max_value or 99999))
            w.setValue(int(self.config.default))
            w.valueChanged.connect(lambda v: self.value_changed.emit(self.config.name, v))
            return w
        elif self.config.type == "enum":
            w = QComboBox()
            w.addItems(self.config.options)
            w.setCurrentText(str(self.config.default))
            w.currentTextChanged.connect(lambda v: self.value_changed.emit(self.config.name, v))
            return w
        elif self.config.type == "bool":
            w = QCheckBox()
            w.setChecked(bool(self.config.default))
            w.stateChanged.connect(lambda v: self.value_changed.emit(self.config.name, bool(v)))
            return w
        else:
            return QLabel(f"Unknown type: {self.config.type}")

    def _on_auto_toggled(self, state):
        # Disable input if auto is checked
        self.input_widget.setEnabled(state == 0)

    def set_value(self, value):
        if self.config.type == "float":
            self.input_widget.setValue(float(value))
        elif self.config.type == "int":
            self.input_widget.setValue(int(value))
        elif self.config.type == "enum":
            self.input_widget.setCurrentText(str(value))
        elif self.config.type == "bool":
            self.input_widget.setChecked(bool(value))

class GroupedAutoWidget(QWidget):
    """Widget for a Grouped Auto control"""
    toggled = Signal(bool)
    
    def __init__(self, config: GroupedAutoConfig, parent=None):
        super().__init__(parent)
        self.config = config
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 5, 0, 5)
        
        self.checkbox = QCheckBox(self.config.label)
        self.checkbox.setStyleSheet("font-weight: bold; color: #4a90e2;") # Make it distinct
        self.checkbox.setChecked(self.config.default_active)
        self.checkbox.toggled.connect(self.toggled)
        
        layout.addWidget(self.checkbox)
        layout.addStretch()

class SectionWidget(QGroupBox):
    """Widget for a Parameter Section"""
    def __init__(self, config: ParameterSectionConfig, parent=None):
        super().__init__(config.title, parent)
        self.config = config
        self.layout = QVBoxLayout(self)
        self.param_widgets: Dict[str, ParameterWidget] = {}
        self.setup_ui()
        
    def setup_ui(self):
        # 1. Grouped Auto (if exists)
        if self.config.grouped_auto and self.config.grouped_auto.enabled:
            self.grouped_auto = GroupedAutoWidget(self.config.grouped_auto)
            self.grouped_auto.toggled.connect(self._on_grouped_auto_toggled)
            self.layout.addWidget(self.grouped_auto)
        
        # 2. Parameters
        for p_config in self.config.parameters:
            pw = ParameterWidget(p_config)
            self.layout.addWidget(pw)
            self.param_widgets[p_config.name] = pw
            
        # Initialize state based on grouped auto default
        if self.config.grouped_auto and self.config.grouped_auto.enabled:
            self._on_grouped_auto_toggled(self.config.grouped_auto.default_active)
            
    def _on_grouped_auto_toggled(self, checked):
        # Enable/Disable controlled parameters
        for param_name in self.config.grouped_auto.controlled_params:
            if param_name in self.param_widgets:
                # If Auto is checked, Input should be DISABLED (usually)
                # Or if Auto is "Active", maybe we disable manual edit? 
                # User said: "easily make a line editor disabled or enabled to not let the user change it if it's auto"
                self.param_widgets[param_name].input_widget.setEnabled(not checked)

class ParameterPanelFactory:
    """Factory to create the full Parameter Panel from a list of SectionConfigs"""
    
    @staticmethod
    def create_panel(sections: List[ParameterSectionConfig]) -> QWidget:
        panel = QWidget()
        main_layout = QHBoxLayout(panel)
        
        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()
        
        # Create sections and add to appropriate layout
        for section_config in sections:
            section_widget = SectionWidget(section_config)
            
            if section_config.position == "left":
                left_layout.addWidget(section_widget)
            else:
                right_layout.addWidget(section_widget)
                
        # Add layouts to main
        main_layout.addLayout(left_layout, 1) # Stretch factor
        main_layout.addLayout(right_layout, 1)
        
        # Add push to top
        left_layout.addStretch()
        right_layout.addStretch()
        
        return panel
