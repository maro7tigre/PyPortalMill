"""
Configure Step

Second step in the wizard: Configure parameters and preview.
Adapted from the old FrameTab with exact same UI but integrated with new architecture.
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QSizePolicy
from PySide6.QtCore import Qt
from PySide6.QtGui import QDoubleValidator

from ui.widgets import (ThemedSplitter, ThemedLabel, ThemedGroupBox, ThemedRadioButton,
                        ThemedSpinBox, ClickableLabel, ScaledPreviewLabel)


class ConfigureStep(QWidget):
    """
    Configuration step with exact same 3-panel layout as old FrameTab.
    
    Layout:
    - Left panel: Frame dimensions, PM positions, parameter preview
    - Middle panel: Orientation selector, preview widget
    - Right panel: Lock config, hinge config, component order
    """
    
    def __init__(self, context: str, parent=None):
        """
        Initialize configure step.
        
        Args:
            context: "frames" or "doors" - determines which parameters to show
            parent: Parent widget
        """
        super().__init__(parent)
        self.context = context
        
        # Auto-calculation control
        self._auto_calculation_running = False
        
        self.setup_ui()
        self.connect_signals()
    
    def setup_ui(self):
        """Initialize user interface with three-panel layout"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(5, 5, 5, 5)
        
        # Content area with splitter
        content_splitter = ThemedSplitter(Qt.Horizontal)
        main_layout.addWidget(content_splitter)
        
        # Left panel
        left_widget = self.create_left_panel()
        content_splitter.addWidget(left_widget)
        
        # Middle panel (preview)
        middle_widget = self.create_middle_panel()
        content_splitter.addWidget(middle_widget)
        
        # Right panel
        right_widget = self.create_right_panel()
        content_splitter.addWidget(right_widget)
        
        # Set initial splitter sizes
        content_splitter.setSizes([300, 400, 300])
    
    def create_left_panel(self):
        """Create left panel with frame dimensions and PM positions"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Frame dimensions group
        frame_group = ThemedGroupBox("Frame Configuration")
        frame_layout = QFormLayout()
        frame_group.setLayout(frame_layout)
        
        # TODO: Add DollarVariableLineEdit widgets for:
        # - Frame height
        # - Frame width
        # - Frame depth
        # - Door width
        # - Hinge width
        # - Machine offsets (x, y, z)
        
        # Placeholder for now
        frame_layout.addRow("Frame Height (mm):", ThemedLabel("TODO: Input"))
        frame_layout.addRow("Frame Width (mm):", ThemedLabel("TODO: Input"))
        
        layout.addWidget(frame_group)
        
        # PM positions group
        pm_group = ThemedGroupBox("PM Positions")
        pm_layout = QVBoxLayout()
        pm_group.setLayout(pm_layout)
        
        # TODO: Add PM auto checkbox and position inputs
        pm_layout.addWidget(ThemedLabel("TODO: PM Controls"))
        
        layout.addWidget(pm_group)
        
        # Parameter preview
        preview_group = ThemedGroupBox("Parameter Preview")
        preview_group.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        preview_layout = QVBoxLayout()
        preview_group.setLayout(preview_layout)
        
        self.param_preview = ScaledPreviewLabel()
        self.param_preview.setText("No preview")
        preview_layout.addWidget(self.param_preview, 1)
        
        layout.addWidget(preview_group, 1)
        
        return widget
    
    def create_middle_panel(self):
        """Create middle panel with preview and orientation switch"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Orientation switch with G-code edit links
        orientation_group = ThemedGroupBox("Door Orientation")
        orientation_layout = QVBoxLayout()
        orientation_group.setLayout(orientation_layout)
        
        # Radio buttons layout
        radio_layout = QHBoxLayout()
        
        # TODO: Use DollarVariableRadioGroup for orientation
        self.right_radio = ThemedRadioButton("Right (droite)")
        self.left_radio = ThemedRadioButton("Left (gauche)")
        
        radio_layout.addWidget(self.right_radio)
        self.right_gcode_link = ClickableLabel("Edit")
        # self.right_gcode_link.clicked.connect(self.edit_right_gcode)
        radio_layout.addWidget(self.right_gcode_link)
        
        radio_layout.addStretch()
        
        radio_layout.addWidget(self.left_radio)
        self.left_gcode_link = ClickableLabel("Edit")
        # self.left_gcode_link.clicked.connect(self.edit_left_gcode)
        radio_layout.addWidget(self.left_gcode_link)
        
        orientation_layout.addLayout(radio_layout)
        
        layout.addWidget(orientation_group)
        
        # Preview area
        # TODO: Add FramePreview widget
        preview_placeholder = ThemedLabel("Preview Widget")
        preview_placeholder.setStyleSheet("QLabel { font-size: 14pt; padding: 20px; background-color: #1e1e1e; }")
        preview_placeholder.setAlignment(Qt.AlignCenter)
        layout.addWidget(preview_placeholder, 1)
        
        return widget
    
    def create_right_panel(self):
        """Create right panel with lock and hinge configuration"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Lock configuration
        lock_group = ThemedGroupBox("Lock Configuration")
        lock_layout = QVBoxLayout()
        lock_group.setLayout(lock_layout)
        
        # TODO: Add lock controls:
        # - Auto checkbox and position
        # - Y offset with auto
        # - Active checkbox
        lock_layout.addWidget(ThemedLabel("TODO: Lock Controls"))
        
        layout.addWidget(lock_group)
        
        # Hinge configuration
        hinge_group = ThemedGroupBox("Hinge Configuration")
        hinge_layout = QVBoxLayout()
        hinge_group.setLayout(hinge_layout)
        
        # Hinge count selector
        count_layout = QHBoxLayout()
        count_layout.addWidget(ThemedLabel("Number of Hinges:"))
        self.hinge_count_spin = ThemedSpinBox()
        self.hinge_count_spin.setRange(0, 4)
        self.hinge_count_spin.setValue(3)
        # self.hinge_count_spin.valueChanged.connect(self.update_hinge_count)
        count_layout.addWidget(self.hinge_count_spin)
        count_layout.addStretch()
        hinge_layout.addLayout(count_layout)
        
        # TODO: Add hinge controls:
        # - Auto checkbox
        # - Position inputs (dynamic based on count)
        # - Y offset with auto
        hinge_layout.addWidget(ThemedLabel("TODO: Hinge Controls"))
        
        layout.addWidget(hinge_group)
        
        # Execution order widget
        order_group = ThemedGroupBox("Component Order")
        order_layout = QVBoxLayout()
        order_group.setLayout(order_layout)
        
        # TODO: Add OrderWidget
        order_layout.addWidget(ThemedLabel("TODO: Order Widget"))
        
        layout.addWidget(order_group, 1)
        
        return widget
    
    def connect_signals(self):
        """Connect widget signals"""
        # TODO: Connect all widget signals
        pass
    
    def run_auto_calculations(self):
        """Run auto-calculation system for dependent parameters"""
        # TODO: Implement auto-calculation logic from old FrameTab
        # This includes: lock position, hinge positions, PM positions, Y offsets
        pass
    
    def update_preview(self):
        """Update the preview widget with current parameters"""
        # TODO: Implement preview update logic
        pass
