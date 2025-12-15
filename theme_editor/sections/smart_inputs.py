"""
Smart Inputs Section
Configuration for composite smart widgets.
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from ..base_section import ThemeEditorSection
from widgets.smart_inputs import (
    AutoInputWidget,
    AutoActiveInputWidget,
    ActiveAttributeWidget, 
    MultiAttributeWidget
)
from widgets.primitives.inputs import ThemedLineEdit

class SmartInputsSection(ThemeEditorSection):
    def setup_config_ui(self):
        self.add_header("General Spacing")
        self.add_number_control("Global Spacing (px)", "layouts.smart_inputs.spacing", 10, 0, 50)
        
        # We can add more specific controls if the widget supports them
        # self.add_number_control("Auto-Label Gap", "layouts.smart_inputs.gap_auto_label", 10, 0, 50)
        # But first let's ensure the "Global Spacing" works effectively.
        
        self.add_header("Multi-Attribute Widget")
        self.add_number_control("Indentation (px)", "layouts.multi_attribute.indent", 10, 0, 50)
        self.add_number_control("Item Spacing (px)", "layouts.multi_attribute.spacing", 5, 0, 30)

    def setup_preview_ui(self):
        layout = self.preview_inner_layout
        
        # Auto + Active combined widget (matches old frame_tab pattern)
        auto_active = AutoActiveInputWidget(
            "Position:",
            ThemedLineEdit("1058"),
            "demo_auto_param",
            "demo_active_param"
        )
        layout.addWidget(auto_active)
        
        # Auto Input Preview (just Auto)
        auto_input = AutoInputWidget(
            ThemedLineEdit("Auto Controlled Input"), 
            "demo_auto_param2"
        )
        layout.addWidget(auto_input)
        
        # Active Attribute Preview
        active_input = ActiveAttributeWidget(
            ThemedLineEdit("Optional Input"),
            "demo_active_param2"
        )
        layout.addWidget(active_input)
        
        # Multi Attribute with Auto checkbox
        def dummy_factory(i):
            return ThemedLineEdit(f"Item #{i}")
        
        multi = MultiAttributeWidget(
            "demo_count_param",
            dummy_factory,
            min_count=0,
            max_count=3,
            auto_param_name="demo_multi_auto",
            auto_label="Auto-position"
        )
        layout.addWidget(multi)

        layout.addStretch()
