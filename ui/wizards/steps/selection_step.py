"""
Selection Step

First step in the wizard: Select hardware profiles (hinges, locks).
Adapted from the old ProfileTab with exact same UI but integrated with new architecture.
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from PySide6.QtCore import Signal, Qt

from ui.widgets import ThemedSplitter, ThemedLabel, ProfileGrid


class SelectionStep(QWidget):
    """
    Profile selection step with exact same interface as old ProfileTab.
    
    Features:
    - Split view with profile grids (hinges left, locks right)
    - Bottom status bar with selection display
    """
    
    # Signals
    profiles_selected = Signal(str, str)  # (hinge_profile, lock_profile)
    
    def __init__(self, context: str, parent=None):
        """
        Initialize selection step.
        
        Args:
            context: "frames" or "doors" - determines which profiles to show
            parent: Parent widget
        """
        super().__init__(parent)
        self.context = context
        self.selected_hinge = None
        self.selected_lock = None
        
        # Protection flag
        self._updating_from_manager = False
        
        self.setup_ui()
        self.connect_signals()
    
    def setup_ui(self):
        """Setup the UI with profile grids"""
        # Main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Middle section - profile grids (takes all space)
        middle_widget = self.create_middle_section()
        layout.addWidget(middle_widget, 1)
        
        # Bottom section - selection display
        bottom_layout = self.create_bottom_section()
        layout.addLayout(bottom_layout)
    
    def create_middle_section(self):
        """Create middle section with profile grids"""
        # Themed splitter
        splitter = ThemedSplitter(Qt.Horizontal)
        
        # Left side - Hinge Profiles
        # TODO: Get ProfileEditor class from dialogs
        self.hinge_grid = ProfileGrid("hinge", None)
        self.hinge_grid.profile_selected.connect(self.on_profile_selected)
        self.hinge_grid.profile_deleted.connect(self.on_profile_deleted)
        splitter.addWidget(self.hinge_grid)
        
        # Right side - Lock Profiles
        self.lock_grid = ProfileGrid("lock", None)
        self.lock_grid.profile_selected.connect(self.on_profile_selected)
        self.lock_grid.profile_deleted.connect(self.on_profile_deleted)
        splitter.addWidget(self.lock_grid)
        
        # Set equal sizes
        splitter.setSizes([400, 400])
        
        return splitter
    
    def create_bottom_section(self):
        """Create bottom section with selection label"""
        bottom_layout = QHBoxLayout()
        
        # Selection label on left
        self.selection_label = ThemedLabel("Selected: [Hinge: None] [Lock: None]")
        self.selection_label.setStyleSheet("QLabel { font-weight: bold; padding: 5px; }")
        bottom_layout.addWidget(self.selection_label)
        
        bottom_layout.addStretch()
        
        return bottom_layout
    
    def connect_signals(self):
        """Connect UI signals"""
        pass
    
    def on_profile_selected(self, profile_type, profile_name):
        """Handle profile selection from grids"""
        if profile_type == "hinge":
            self.selected_hinge = profile_name
        elif profile_type == "lock":
            self.selected_lock = profile_name
        
        self.update_selection_display()
        
        # Emit signal when both selected
        if self.selected_hinge and self.selected_lock:
            self.profiles_selected.emit(self.selected_hinge, self.selected_lock)
    
    def on_profile_deleted(self, profile_type, profile_name):
        """Handle profile deletion from grids"""
        # TODO: Update ProjectManager to delete profile
        print(f"Delete profile requested: {profile_type} - {profile_name}")
        
        # Clear selection if deleted profile was selected
        if profile_type == "hinge" and self.selected_hinge == profile_name:
            self.selected_hinge = None
        elif profile_type == "lock" and self.selected_lock == profile_name:
            self.selected_lock = None
        
        self.update_selection_display()
    
    def update_selection_display(self):
        """Update selection label"""
        hinge_text = self.selected_hinge or "None"
        lock_text = self.selected_lock or "None"
        self.selection_label.setText(f"Selected: [Hinge: {hinge_text}] [Lock: {lock_text}]")
    
    def update_profiles(self, hinge_profiles, lock_profiles):
        """Update grids with profile data from ProjectManager"""
        self._updating_from_manager = True
        try:
            self.hinge_grid.update_profiles(hinge_profiles, self.selected_hinge)
            self.lock_grid.update_profiles(lock_profiles, self.selected_lock)
        finally:
            self._updating_from_manager = False
    
    def get_selected_profiles(self):
        """Get currently selected profiles"""
        return {
            'hinge': self.selected_hinge,
            'lock': self.selected_lock
        }
    
    def set_selected_profiles(self, hinge, lock):
        """Set selected profiles (for loading projects)"""
        self._updating_from_manager = True
        try:
            self.selected_hinge = hinge
            self.selected_lock = lock
            self.update_selection_display()
            # Update grid selection states
            self.hinge_grid.selected_profile = hinge
            self.hinge_grid.update_selection_states()
            self.lock_grid.selected_profile = lock
            self.lock_grid.update_selection_states()
        finally:
            self._updating_from_manager = False

