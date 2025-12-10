"""
Configure Step

Second step in the wizard: Configure parameters and preview.
Fully data-driven based on TabConfig.
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QSizePolicy, QScrollArea
from PySide6.QtCore import Qt
from PySide6.QtGui import QDoubleValidator

from ui.widgets import (ThemedSplitter, ThemedLabel, ThemedGroupBox, ThemedRadioButton,
                        ThemedSpinBox, ClickableLabel, ScaledPreviewLabel)
from ui.widgets.parameter_factory import SectionWidget
from core.config_manager import TabConfig

class ConfigureStep(QWidget):
    """
    Configuration step with 3-panel layout.
    
    Layout:
    - Left panel: Parameters configured with position="left"
    - Middle panel: Orientation selector, preview widget
    - Right panel: Parameters configured with position="right"
    """
    
    def __init__(self, context: str, tab_config: TabConfig, parent=None):
        """
        Initialize configure step.
        
        Args:
            context: Context string (e.g. "doors", "frames")
            tab_config: Configuration object for this tab
            parent: Parent widget
        """
        super().__init__(parent)
        self.context = context
        self.tab_config = tab_config
        
        self.setup_ui()
    
    def setup_ui(self):
        """Initialize user interface with three-panel layout"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(5, 5, 5, 5)
        
        # Content area with splitter
        content_splitter = ThemedSplitter(Qt.Horizontal)
        main_layout.addWidget(content_splitter)
        
        # Left panel (Scrollable)
        left_scroll = QScrollArea()
        left_scroll.setWidgetResizable(True)
        left_scroll.setFrameShape(QScrollArea.NoFrame)
        left_content = QWidget()
        self.left_layout = QVBoxLayout(left_content)
        self.left_layout.setContentsMargins(0,0,10,0)
        left_scroll.setWidget(left_content)
        
        # Middle panel (Fixed/Preview)
        middle_widget = self.create_middle_panel()
        
        # Right panel (Scrollable)
        right_scroll = QScrollArea()
        right_scroll.setWidgetResizable(True)
        right_scroll.setFrameShape(QScrollArea.NoFrame)
        right_content = QWidget()
        self.right_layout = QVBoxLayout(right_content)
        self.right_layout.setContentsMargins(10,0,0,0)
        right_scroll.setWidget(right_content)
        
        # Add widgets to splitter
        content_splitter.addWidget(left_scroll)
        content_splitter.addWidget(middle_widget)
        content_splitter.addWidget(right_scroll)
        
        # Set initial splitter sizes
        content_splitter.setSizes([350, 400, 350])
        
        # Populate parameter sections
        self.populate_sections()
        
    def populate_sections(self):
        """Populate left and right panels with sections from config"""
        for section_config in self.tab_config.parameter_sections:
            section_widget = SectionWidget(section_config)
            
            if section_config.position == "left":
                self.left_layout.addWidget(section_widget)
            else:
                self.right_layout.addWidget(section_widget)
                
        # Add stretch to push content to top
        self.left_layout.addStretch()
        self.right_layout.addStretch()
    
    def create_middle_panel(self):
        """Create middle panel with preview and orientation switch"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(10, 0, 10, 0)
        
        # Orientation (Hardcoded for now as it seems standard, but could be config too)
        # Only show if not specifically disabled in config, or we just leave it as Standard UI
        orientation_group = ThemedGroupBox("Orientation")
        orientation_layout = QVBoxLayout()
        orientation_group.setLayout(orientation_layout)
        
        radio_layout = QHBoxLayout()
        self.right_radio = ThemedRadioButton("Right (Standard)")
        self.left_radio = ThemedRadioButton("Left (Reverse)")
        
        radio_layout.addWidget(self.right_radio)
        radio_layout.addStretch()
        radio_layout.addWidget(self.left_radio)
        
        orientation_layout.addLayout(radio_layout)
        layout.addWidget(orientation_group)
        
        # Preview Area
        preview_group = ThemedGroupBox("Preview")
        preview_layout = QVBoxLayout()
        preview_group.setLayout(preview_layout)
        
        # Placeholder or Real Preview
        self.preview_label = ScaledPreviewLabel()
        self.preview_label.setText("No Preview")
        preview_layout.addWidget(self.preview_label, 1)
        
        layout.addWidget(preview_group, 1)
        
        return widget
