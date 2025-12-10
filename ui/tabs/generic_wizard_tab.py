"""
Generic Wizard Tab
A generic tab implementation that configures itself based on TabConfig.
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTabWidget
from PySide6.QtCore import Qt
from ui.wizards.steps import SelectionStep, ConfigureStep, GenerateStep
from ui.widgets import ThemedButton
from core.config_manager import TabConfig

class GenericWizardTab(QWidget):
    """
    Generic Tab containing:
    - 3-tab widget (Profiles/Selection, Setup/Configure, Export/Generate)
    - Back/Next navigation buttons
    - Configures content based on TabConfig
    """
    
    def __init__(self, tab_config: TabConfig, parent=None):
        super().__init__(parent)
        self.tab_config = tab_config
        self.context = tab_config.id
        self.setup_ui()
        self.connect_signals()
    
    def setup_ui(self):
        """Setup the tab UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)
        
        # Tab widget with 3 tabs
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabPosition(QTabWidget.North)  # Tabs at top
        
        # Create step widgets with configuration
        # pass tab_config to steps so they know what to render
        self.selection_step = SelectionStep(context=self.context, tab_config=self.tab_config)
        self.configure_step = ConfigureStep(context=self.context, tab_config=self.tab_config)
        self.generate_step = GenerateStep(context=self.context) # Generate might just need context
        
        # Add tabs
        self.tab_widget.addTab(self.selection_step, "1. Profiles/Selection")
        self.tab_widget.addTab(self.configure_step, "2. Setup/Configure")
        self.tab_widget.addTab(self.generate_step, "3. Export/Generate")
        
        layout.addWidget(self.tab_widget)
        
        # Navigation buttons at bottom
        nav_layout = self.create_navigation()
        layout.addLayout(nav_layout)
    
    def create_navigation(self) -> QHBoxLayout:
        """Create navigation buttons (Back/Next)"""
        nav_layout = QHBoxLayout()
        nav_layout.setContentsMargins(10, 5, 10, 5)
        
        # Back button
        self.back_button = ThemedButton("← Back", button_type="secondary")
        nav_layout.addWidget(self.back_button)
        
        nav_layout.addStretch()
        
        # Next/Finish button
        self.next_button = ThemedButton("Next →", button_type="primary")
        nav_layout.addWidget(self.next_button)
        
        self.update_navigation_buttons()
        return nav_layout
    
    def connect_signals(self):
        """Connect signals"""
        self.back_button.clicked.connect(self.prev_tab)
        self.next_button.clicked.connect(self.next_tab)
        self.tab_widget.currentChanged.connect(self.update_navigation_buttons)
    
    def next_tab(self):
        current = self.tab_widget.currentIndex()
        if current < self.tab_widget.count() - 1:
            self.tab_widget.setCurrentIndex(current + 1)
    
    def prev_tab(self):
        current = self.tab_widget.currentIndex()
        if current > 0:
            self.tab_widget.setCurrentIndex(current - 1)
    
    def update_navigation_buttons(self):
        current = self.tab_widget.currentIndex()
        total = self.tab_widget.count()
        
        self.back_button.setEnabled(current > 0)
        
        if current == total - 1:
            self.next_button.setText("Finish ✓")
        else:
            self.next_button.setText("Next →")
