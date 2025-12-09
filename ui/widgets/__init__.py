"""
Widgets Package

Reusable widget components for PyPortalMill.
"""

# Themed widgets
from .themed_widgets import (
    ThemedButton, PurpleButton, GreenButton, BlueButton, OrangeButton,
    ThemedLineEdit, ThemedTextEdit, ThemedSpinBox, ThemedDoubleSpinBox,
    ThemedGroupBox, ThemedLabel, ThemedCheckBox, ThemedRadioButton,
    ThemedScrollArea, ThemedSplitter, ThemedListWidget, ThemedMenu
)

# Simple widgets
from .simple_widgets import (
    ClickableLabel, ScaledImageLabel, ClickableImageLabel,
    ScaledPreviewLabel, ErrorLineEdit, PlaceholderPixmap
)

# Dollar variable widgets  
from .dollar_variable_widgets import (
    DollarVariableLineEdit, DollarVariableSpinBox,
    DollarVariableCheckBox, DollarVariableRadioGroup
)

# Profile widgets
from .profile_item import ProfileItem
from .profile_grid import ProfileGrid

# Complex editors
from .variable_editor import VariableEditor
from .custom_editor import CustomEditor


__all__ = [
    # Themed widgets
    'ThemedButton', 'PurpleButton', 'GreenButton', 'BlueButton', 'OrangeButton',
    'ThemedLineEdit', 'ThemedTextEdit', 'ThemedSpinBox', 'ThemedDoubleSpinBox',
    'ThemedGroupBox', 'ThemedLabel', 'ThemedCheckBox', 'ThemedRadioButton',
    'ThemedScrollArea', 'ThemedSplitter', 'ThemedListWidget', 'ThemedMenu',
    
    # Simple widgets
    'ClickableLabel', 'ScaledImageLabel', 'ClickableImageLabel',
    'ScaledPreviewLabel', 'ErrorLineEdit', 'PlaceholderPixmap',
    
    # Dollar variable widgets
    'DollarVariableLineEdit', 'DollarVariableSpinBox',
    'DollarVariableCheckBox', 'DollarVariableRadioGroup',
    
    # Profile widgets
    'ProfileItem', 'ProfileGrid',
    
    # Complex editors
    'VariableEditor', 'CustomEditor'
]

