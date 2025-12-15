"""
Widget Factory
Creates widgets based on dictionary configurations.
"""

from PySide6.QtGui import QDoubleValidator

from .variable_inputs import (
    DollarVariableLineEdit, 
    DollarVariableSpinBox, 
    DollarVariableCheckBox,
    DollarVariableRadioGroup
)
from .smart_inputs import (
    AutoInputWidget, 
    ActiveAttributeWidget, 
    MultiAttributeWidget
)
from .primitives.labels import ThemedLabel

class WidgetFactory:
    """Factory for creating widgets from configuration"""
    
    @staticmethod
    def create_widget(config: dict, parent=None):
        """
        Create a widget based on the configuration dictionary.
        Handles 'type', 'auto', 'active' wrappers.
        """
        widget_type = config.get('type', 'string')
        param_name = config.get('parameter_name', '')
        display_name = config.get('display_name', param_name)
        
        # 1. Handle Multi-Attribute Special Case
        if widget_type == 'multi_attribute':
            return WidgetFactory._create_multi_attribute(config, parent)
            
        # 2. Create Base Widget
        base_widget = WidgetFactory._create_base_widget(widget_type, param_name, config, parent)
        
        # 3. Wrap in Auto if needed
        if config.get('auto'):
            base_widget = AutoInputWidget(base_widget, param_name + "_auto", parent)
            
        # 4. Wrap in Active if needed
        # Note: If validation/logic requires 'Active' wrapper. 
        # Sometimes 'active' just means it has a checkbox to enable it.
        # If the widget itself IS the toggle (like a checkbox), we don't wrap it.
        if config.get('active') and widget_type != 'bool':
            # Check if we have a specific active parameter name, otherwise append _active
            active_param = config.get('active_parameter_name', param_name + "_active")
            base_widget = ActiveAttributeWidget(base_widget, active_param, "Active", parent)
            
        return base_widget

    @staticmethod
    def _create_base_widget(widget_type, param_name, config, parent):
        """Create the inner primitive widget"""
        
        if widget_type in ['float', 'int', 'string']:
            # Use LineEdit for numbers to allow exact formatting, or SpinBox for Ints
            # But the user requirements often used LineEdits with Validators in old code.
            # We'll use DollarVariableLineEdit for flexibility unless strictly 'int' with range.
            
            widget = DollarVariableLineEdit(param_name, parent=parent)
            
            # Apply Validator
            if widget_type in ['float', 'int']:
                min_val = config.get('min', -10000)
                max_val = config.get('max', 10000)
                decimals = 2 if widget_type == 'float' else 0
                
                validator = QDoubleValidator(float(min_val), float(max_val), decimals)
                validator.setNotation(QDoubleValidator.StandardNotation)
                widget.setValidator(validator)
                
            return widget
            
        elif widget_type == 'bool':
            label = config.get('display_name', '')
            # If it's a simple bool, it's just a checkbox
            return DollarVariableCheckBox(param_name, label, parent=parent)
            
        elif widget_type == 'profile_grid':
            # This is complex and might be handled by the Section, but if we need it here:
            from .components.lists import ProfileGrid
            # ProfileGrid requires profile_name to know what to load
            return ProfileGrid(param_name, parent=parent)
            
        elif widget_type == 'image_preview':
            from .components.image_preview import ImagePreviewWidget # Assuming this exists or will exist
            # If not, use placeholder
            return ThemedLabel("Image Preview Placeholder")
            
        else:
            return ThemedLabel(f"Unknown type: {widget_type}")

    @staticmethod
    def _create_multi_attribute(config, parent):
        """Create a MultiAttributeWidget with template factory"""
        count_param = config.get('count_parameter', config.get('parameter_name') + "_count")
        min_count = config.get('min', 0)
        max_count = config.get('max', 10)
        template = config.get('template', {})
        
        def template_factory(index):
            # 1. Deep copy template to avoid modifying original
            import copy
            item_config = copy.deepcopy(template)
            
            # 2. Replace placeholders
            # Replace '#' in parameter_name and display_name
            if 'parameter_name' in item_config:
                item_config['parameter_name'] = item_config['parameter_name'].replace('#', str(index))
            
            if 'display_name' in item_config:
                # If display name is a dict (localized), update internal strings?
                # Or if string, update directly.
                dn = item_config.get('display_name')
                if isinstance(dn, str):
                    item_config['display_name'] = dn.replace('#', str(index))
            
            # 3. Create widget recursively
            return WidgetFactory.create_widget(item_config)
            
        return MultiAttributeWidget(
            count_param_name=count_param,
            template_factory_func=template_factory,
            min_count=min_count,
            max_count=max_count,
            parent=parent
        )
