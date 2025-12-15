"""
Smart Input Widgets

This module contains composite widgets that handle complex logic like
Auto-calculation enabling/disabling, Active state toggling, and 
Multi-attribute spawning.
"""

from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QGroupBox
from PySide6.QtCore import Signal, Qt

from .primitives.inputs import ThemedCheckBox, ThemedSpinBox, ThemedLineEdit
from .primitives.labels import ThemedLabel
from .primitives.containers import ThemedGroupBox
from .primitives.containers import ThemedGroupBox
from .variable_inputs import DollarVariableCheckBox, DollarVariableSpinBox, DollarVariableLineEdit
from .mixins import ThemedWidgetMixin
from core.theme_manager import get_theme_manager

class AutoInputWidget(QWidget, ThemedWidgetMixin):
    """
    Composite widget with a 'Auto' checkbox and an input field.
    When 'Auto' is checked, the input field is disabled (read-only) and 
    its value is derived from a calculation method.
    """
    
    def __init__(self, 
                 input_widget: QWidget, 
                 auto_param_name: str, 
                 parent=None):
        super().__init__(parent)
        ThemedWidgetMixin.__init__(self)
        self.input_widget = input_widget
        self.auto_param_name = auto_param_name
        
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(10)
        
        # Auto Checkbox
        self.auto_checkbox = DollarVariableCheckBox(
            variable_name=auto_param_name, 
            text="Auto"
        )
        self.auto_checkbox.stateChanged.connect(self._on_auto_toggled)
        
        self.layout.addWidget(self.auto_checkbox)
        self.layout.addWidget(self.input_widget, 1) # Input takes remaining space
        
        # Initial state update (defer slightly to let main_window connection happen if needed)
        # But for now, just set based on current check state which might have loaded default
        self._update_input_state()

    def set_main_window(self, main_window):
        """Pass main_window to children"""
        if hasattr(self.auto_checkbox, 'main_window'):
            self.auto_checkbox.main_window = main_window
            self.auto_checkbox.update_from_main_window()
            
        if hasattr(self.input_widget, 'main_window'):
            self.input_widget.main_window = main_window
            if hasattr(self.input_widget, 'update_from_main_window'):
                self.input_widget.update_from_main_window()
        
        # Update state after main_window is set
        self._on_auto_toggled(self.auto_checkbox.checkState())

    def _on_auto_toggled(self, state):
        """Enable/Disable input based on Auto state"""
        is_auto = (state == Qt.Checked)
        self.input_widget.setEnabled(not is_auto)
        
        # Optional: Add visual cue for auto state
        self._update_input_state()
        
    def _update_input_state(self):
        is_auto = self.auto_checkbox.isChecked()
        self.input_widget.setEnabled(not is_auto)
        # TODO: Trigger calculation if auto is enabled? 
        # Usually handled by the ConfigManager listening to the variable change.


class AutoActiveInputWidget(QWidget, ThemedWidgetMixin):
    """
    Combined widget: [Auto Checkbox] [Label] [Input] [Active Checkbox]
    All in one horizontal row. Replicates the old frame_tab pattern.
    """
    
    def __init__(self,
                 label_text: str,
                 input_widget: QWidget,
                 auto_param_name: str,
                 active_param_name: str = None,
                 parent=None):
        super().__init__(parent)
        ThemedWidgetMixin.__init__(self)
        self.input_widget = input_widget
        self.auto_param_name = auto_param_name
        self.active_param_name = active_param_name
        
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(10)
        
        # Auto Checkbox
        self.auto_checkbox = DollarVariableCheckBox(
            variable_name=auto_param_name,
            text="Auto"
        )
        self.auto_checkbox.stateChanged.connect(self._on_auto_toggled)
        self.layout.addWidget(self.auto_checkbox)
        
        # Label
        self.label = ThemedLabel(label_text)
        self.layout.addWidget(self.label)
        
        # Input Widget (takes remaining space)
        self.layout.addWidget(input_widget, 1)
        
        # Active Checkbox (optional)
        if active_param_name:
            self.active_checkbox = DollarVariableCheckBox(
                variable_name=active_param_name,
                text="Active"
            )
            self.layout.addWidget(self.active_checkbox)
        else:
            self.active_checkbox = None
        
        self.update_style()
        self._update_input_state()
    
    def set_main_window(self, main_window):
        """Pass main_window to children"""
        if hasattr(self.auto_checkbox, 'main_window'):
            self.auto_checkbox.main_window = main_window
            self.auto_checkbox.update_from_main_window()
        
        if self.active_checkbox and hasattr(self.active_checkbox, 'main_window'):
            self.active_checkbox.main_window = main_window
            self.active_checkbox.update_from_main_window()
            
        if hasattr(self.input_widget, 'main_window'):
            self.input_widget.main_window = main_window
            if hasattr(self.input_widget, 'update_from_main_window'):
                self.input_widget.update_from_main_window()
        
        self._on_auto_toggled(self.auto_checkbox.checkState())
    
    def _on_auto_toggled(self, state):
        """
        Enable/Disable input based on Auto state.
        This must be robust to ensure inputs are actually disabled.
        """
        is_auto = (state == Qt.Checked)
        self.input_widget.setEnabled(not is_auto)
        self._update_input_state()
    
    def _update_input_state(self):
        is_auto = self.auto_checkbox.isChecked()
        self.input_widget.setEnabled(not is_auto)
    
    def on_theme_changed(self, theme_name):
        self.update_style()
    
    def update_style(self):
        tm = get_theme_manager()
        
        # Granular Spacing
        # 1. Spacing for the main layout (gap between elements)
        # Or better: use specific margins/spacers if QHBoxLayout doesn't support per-item spacing.
        # QHBoxLayout uses 'spacing' for all gaps. 
        # For now, we'll control the global spacing of this widget more granularly if requested,
        # but QHBoxLayout has one spacing value.
        
        spacing = tm.get_style("layouts.smart_inputs.spacing")
        if spacing is None: spacing = 10
        self.layout.setSpacing(int(spacing))
        
        # If we pushed for "space between auto and label" vs "label and input", we'd need manual spacers.
        # But user asked for "space between auto, line edit and active".
        # Let's try to interpret this as just general spacing first, but ensure it UPDATES correctly.
        # The user said "configuration has no effect and is laggy".
        # Ensure we convert to int and actually set it.
        
        # Debug print or ensure value is correct
        # print(f"Setting spacing to {spacing}")


class ActiveAttributeWidget(QWidget, ThemedWidgetMixin):
    """
    Composite widget with content and an 'Active' checkbox to the right.
    Used for optional features (e.g., 'Active' checkbox for a lock).
    Layout: [Content Widget] [Active Checkbox]
    """
    
    def __init__(self, 
                 content_widget: QWidget, 
                 active_param_name: str, 
                 label_text: str = "Active",
                 parent=None):
        super().__init__(parent)
        ThemedWidgetMixin.__init__(self)
        self.content_widget = content_widget
        
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        
        # Content first (takes up most space)
        if content_widget:
            self.layout.addWidget(content_widget, 1)
        
        # Active Checkbox to the right
        self.active_checkbox = DollarVariableCheckBox(
            variable_name=active_param_name,
            text=label_text
        )
        self.active_checkbox.stateChanged.connect(self._on_active_toggled)
        self.layout.addWidget(self.active_checkbox)
            
        self._update_content_state()
        self.update_style()
        
    def on_theme_changed(self, theme_name):
        self.update_style()
        
    def update_style(self):
        tm = get_theme_manager()
        spacing = tm.get_style("layouts.smart_inputs.spacing")
        if spacing is None: spacing = 10
        self.layout.setSpacing(int(spacing))

    def set_main_window(self, main_window):
        if hasattr(self.active_checkbox, 'main_window'):
            self.active_checkbox.main_window = main_window
            self.active_checkbox.update_from_main_window()
            
        if self.content_widget and hasattr(self.content_widget, 'main_window'):
            self.content_widget.main_window = main_window
            if hasattr(self.content_widget, 'update_from_main_window'):
                self.content_widget.update_from_main_window()
                
        self._on_active_toggled(self.active_checkbox.checkState())

    def _on_active_toggled(self, state):
        """When Active is toggled, show/hide content widget"""
        is_active = (state == Qt.Checked)
        if self.content_widget:
            self.content_widget.setVisible(is_active)
            
    def _update_content_state(self):
        is_active = self.active_checkbox.isChecked()
        if self.content_widget:
            self.content_widget.setVisible(is_active)


class MultiAttributeWidget(QWidget, ThemedWidgetMixin):
    """
    Dynamic widget that spawns N instances of a template attribute
    based on a count (SpinBox).
    Optional: Add an Auto checkbox to enable/disable all.
    """
    
    def __init__(self, 
                 count_param_name: str, 
                 template_factory_func, # Function that takes (index) and returns a widget
                 min_count=0, 
                 max_count=10,
                 auto_param_name: str = None,  # Optional: parameter for Auto checkbox
                 auto_label: str = "Auto-position",
                 parent=None):
        super().__init__(parent)
        ThemedWidgetMixin.__init__(self)
        self.template_factory = template_factory_func
        self.instances = []
        self.main_window = None
        self.auto_param_name = auto_param_name
        
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        
        # Count Control
        header_layout = QHBoxLayout()
        header_layout.addWidget(ThemedLabel("Count:"))
        
        self.count_spin = DollarVariableSpinBox(variable_name=count_param_name)
        self.count_spin.setRange(min_count, max_count)
        self.count_spin.valueChanged.connect(self._on_count_changed)
        header_layout.addWidget(self.count_spin)
        header_layout.addStretch()
        
        self.layout.addLayout(header_layout)
        
        # Optional Auto Checkbox
        if auto_param_name:
            self.auto_checkbox = DollarVariableCheckBox(
                variable_name=auto_param_name,
                text=auto_label
            )
            # Connect auto toggle to enable/disable logic
            self.auto_checkbox.stateChanged.connect(self._on_auto_toggled)
            self.layout.addWidget(self.auto_checkbox)
        else:
            self.auto_checkbox = None
        
        # Container for instances
        self.instance_container = QWidget()
        self.instance_layout = QVBoxLayout(self.instance_container)
        self.instance_layout.setContentsMargins(10, 0, 0, 0) # Indent children
        self.layout.addWidget(self.instance_container)
        self.update_style()
        
    def on_theme_changed(self, theme_name):
        self.update_style()
        
    def update_style(self):
        tm = get_theme_manager()
        indent = tm.get_style("layouts.multi_attribute.indent")
        if indent is None: indent = 10
        self.instance_layout.setContentsMargins(int(indent), 0, 0, 0)
        
        spacing = tm.get_style("layouts.multi_attribute.spacing")
        if spacing is None: spacing = 5
        self.instance_layout.setSpacing(int(spacing))

    def set_main_window(self, main_window):
        self.main_window = main_window
        self.count_spin.main_window = main_window
        self.count_spin.update_from_main_window()
        
        if self.auto_checkbox:
            self.auto_checkbox.main_window = main_window
            self.auto_checkbox.update_from_main_window()
            # Initial auto state check
            self._on_auto_toggled(self.auto_checkbox.checkState())
        
        # Trigger initial build based on CURRENT value from main_window
        initial_count = self.count_spin.value()
        if initial_count > 0:
            self._on_count_changed(initial_count)

    def _on_auto_toggled(self, state):
        """Enable/Disable all instances based on auto state"""
        is_auto = (state == Qt.Checked)
        # Iterate over all instances and disable/enable them
        self.instance_container.setEnabled(not is_auto)
        # Alternatively, disable individual widgets if container disabling style is not desired (e.g., greyed out look)
        # But usually disabling container is best.

    def _on_count_changed(self, count):
        """Rebuild instances to match count"""
        current_count = len(self.instances)
        
        if count > current_count:
            # Add missing instances
            for i in range(current_count, count):
                widget = self.template_factory(i + 1) # 1-based index for logic usually
                if self.main_window and hasattr(widget, 'set_main_window'):
                    widget.set_main_window(self.main_window)
                elif self.main_window and hasattr(widget, 'main_window'): # Direct attribute support
                     widget.main_window = self.main_window
                     if hasattr(widget, 'update_from_main_window'):
                         widget.update_from_main_window()
                         
                self.instance_layout.addWidget(widget)
                self.instances.append(widget)
                
        elif count < current_count:
            # Remove excess instances
            for i in range(current_count - 1, count - 1, -1):
                widget = self.instances.pop()
                widget.deleteLater()


# GroupedAutoSection has been removed - just use ThemedGroupBox directly for visual grouping
# The "Auto" logic for groups of widgets should be handled by the ConfigManager
# or by individual AutoInputWidgets responding to their own auto parameters
