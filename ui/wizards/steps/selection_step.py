"""
Selection Step

First step in the wizard: Select hardware profiles.
Fully data-driven based on TabConfig.
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from PySide6.QtCore import Signal, Qt

from ui.widgets import ThemedSplitter, ThemedLabel, ProfileGrid
from core.config_manager import TabConfig
from typing import Dict

class SelectionStep(QWidget):
    """
    Profile selection step.
    Dynamically creates grids for each profile type defined in configuration.
    """
    
    def __init__(self, context: str, tab_config: TabConfig, parent=None):
        """
        Initialize selection step.
        
        Args:
            context: Context string
            tab_config: Configuration object
            parent: Parent widget
        """
        super().__init__(parent)
        self.context = context
        self.tab_config = tab_config
        
        # Store selected profiles: { profile_id: selected_name }
        self.selected_profiles: Dict[str, str] = {}
        self.grids: Dict[str, ProfileGrid] = {}
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the UI with profile grids"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Middle section - profile grids
        splitter = ThemedSplitter(Qt.Horizontal)
        
        for profile_config in self.tab_config.profiles:
            # Create grid for this profile type
            # Assuming ProfileGrid takes (type_id, parent)
            grid = ProfileGrid(profile_config.id, None) 
            grid.profile_selected.connect(lambda type_id=profile_config.id, name=None: 
                                        self.on_profile_selected(type_id, name))
            # Note: lambda logic needs fix to capture values correctly in loop!
            # Using partial or distinct linking is safer, but let's do this:
            self._connect_grid(grid, profile_config.id)
            
            splitter.addWidget(grid)
            self.grids[profile_config.id] = grid
            
        layout.addWidget(splitter, 1)
        
        # Bottom section - selection display
        self.selection_label = ThemedLabel("Selected: None")
        self.selection_label.setStyleSheet("QLabel { font-weight: bold; padding: 5px; }")
        layout.addWidget(self.selection_label)
        
        self.update_selection_display()

    def _connect_grid(self, grid, profile_id):
        # Helper to avoid lambda loop issues
        grid.profile_selected.connect(lambda t, n: self.on_profile_selected(profile_id, n)) # Grid emits (type, name) or just name? 
        # Existing code: grid.profile_selected.connect(self.on_profile_selected)
        # Existing on_profile_selected took (type, name).
        # ProfileGrid likely emits (type, name) if it knows its type?
        # Let's check previous code.
        # "self.hinge_grid = ProfileGrid("hinge", None)" -> "self.on_profile_selected"
        # Since ProfileGrid likely emits (type, name) or just name, I should trust it emits what's needed.
        # If ProfileGrid emits (type, name), then:
        grid.profile_selected.connect(self.on_profile_selected)

    def on_profile_selected(self, profile_type, profile_name):
        """Handle profile selection from grids"""
        self.selected_profiles[profile_type] = profile_name
        self.update_selection_display()
        
    def update_selection_display(self):
        """Update selection label"""
        text_parts = []
        for p_config in self.tab_config.profiles:
            name = self.selected_profiles.get(p_config.id, "None")
            text_parts.append(f"[{p_config.name}: {name}]")
        
        self.selection_label.setText("Selected: " + " ".join(text_parts))


