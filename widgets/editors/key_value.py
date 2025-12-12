"""
Key-Value Editors Module

Editors for managing key-value pairs (custom variables, L-variables).
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from PySide6.QtCore import Qt
import re
from typing import Dict, Any

from widgets import ThemedLabel, ThemedScrollArea, ThemedLineEdit


class AbstractKeyValueEditor(QWidget):
    """Base class for key-value editors with scrollable area"""
    
    def __init__(self, title: str, parent=None):
        super().__init__(parent)
        self.editors = {}  # key -> line_edit
        self.title_text = title
        
        self.setup_ui()
        self.apply_styling()
    
    def apply_styling(self):
        """Apply Python-based styling"""
        self.setStyleSheet("""
            QWidget {
                background-color: #282a36;
                color: #ffffff;
            }
        """)
    
    def setup_ui(self):
        """Setup UI components"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Title
        self.title_label = ThemedLabel(self.title_text)
        self.title_label.setStyleSheet("QLabel { font-weight: bold; padding: 5px; }")
        layout.addWidget(self.title_label)
        
        # Scroll area - resizable
        scroll = ThemedScrollArea()
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setWidgetResizable(True)
        scroll.setMinimumHeight(100)
        
        # Container
        container = QWidget()
        container.setStyleSheet("QWidget { background-color: #1d1f28; }")
        self.items_layout = QVBoxLayout(container)
        self.items_layout.setSpacing(5)
        self.items_layout.setContentsMargins(5, 5, 5, 5)
        
        scroll.setWidget(container)
        layout.addWidget(scroll, 1)
        
        # Store implementation specific layout wrapper if needed
        # but defaulting to self.items_layout for adding items
    
    def clear_items(self):
        """Clear all editor items"""
        while self.items_layout.count():
            item = self.items_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self.editors.clear()
        
    def get_values(self) -> Dict[str, str]:
        """Get all values as dictionary"""
        values = {}
        for key, line_edit in self.editors.items():
            values[key] = line_edit.text()
        return values
    
    def set_values(self, values: Dict[str, Any]):
        """Set values"""
        for key, value in values.items():
            if key in self.editors:
                self.editors[key].setText(str(value))


class CustomVariableEditor(AbstractKeyValueEditor):
    """Editor for custom variables (excluding L and $ variables)"""
    
    def __init__(self, parent=None):
        super().__init__("Custom Variables", parent)
        
    def update_variables(self, gcode: str):
        """Extract custom variables from gcode and update UI"""
        self.clear_items()
        
        # Find custom variables (not L or $ variables) - parse name:default correctly
        pattern = r'\{([^L$][^:}]*?)(?::([^}]+))?\}'
        matches = re.findall(pattern, gcode)
        
        # Create unique customs
        unique_customs = {}
        for var_name, default in matches:
            if var_name not in unique_customs:
                unique_customs[var_name] = default
        
        # Create editors
        for var_name in sorted(unique_customs.keys()):
            default = unique_customs[var_name]
            
            # Custom widget
            item_widget = QWidget()
            item_layout = QVBoxLayout(item_widget)
            item_layout.setContentsMargins(0, 0, 0, 0)
            
            # Label
            label = ThemedLabel(f"{var_name}:")
            item_layout.addWidget(label)
            
            # Line edit
            line_edit = ThemedLineEdit()
            if default:
                line_edit.setText(default)
            line_edit.setPlaceholderText("Enter value or entire line...")
            item_layout.addWidget(line_edit)
            
            self.items_layout.addWidget(item_widget)
            self.editors[var_name] = line_edit
        
        # Add stretch and update visibility
        self.items_layout.addStretch()
        self.setVisible(len(self.editors) > 0)


class LVariableEditor(AbstractKeyValueEditor):
    """Editor for L variables (L1, L2, etc.)"""
    
    def __init__(self, parent=None):
        super().__init__("Variables (L)", parent)
        
    def _sort_l_variables(self, var_names):
        """Sort L variables numerically"""
        def extract_number(var_name):
            match = re.match(r'L(\d+)', var_name)
            return int(match.group(1)) if match else 0
        return sorted(var_names, key=extract_number)
        
    def update_variables(self, gcode: str):
        """Extract L variables from gcode and update UI"""
        self.clear_items()
        
        # Find L variables {L1} or {L1:default}
        pattern = r'\{(L\d+)(?::([^}]+))?\}'
        matches = re.findall(pattern, gcode)
        
        # Create unique variables
        unique_vars = {}
        for var_name, default in matches:
            if var_name not in unique_vars:
                unique_vars[var_name] = default
        
        # Create editors - Sort numerically
        for var_name in self._sort_l_variables(unique_vars.keys()):
            default = unique_vars[var_name]
            
            # Variable widget
            item_widget = QWidget()
            item_layout = QHBoxLayout(item_widget)
            item_layout.setContentsMargins(0, 0, 0, 0)
            
            # Label
            label = ThemedLabel(f"{var_name}:")
            label.setFixedWidth(60)
            item_layout.addWidget(label)
            
            # Line edit
            line_edit = ThemedLineEdit()
            if default:
                line_edit.setText(default)
            line_edit.setPlaceholderText("Enter value...")
            item_layout.addWidget(line_edit)
            
            self.items_layout.addWidget(item_widget)
            self.editors[var_name] = line_edit
        
        # Add stretch and update visibility
        self.items_layout.addStretch()
        self.setVisible(len(self.editors) > 0)
