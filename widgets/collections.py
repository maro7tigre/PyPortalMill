"""
Collection Widgets Module

Widgets that manage collections of items (Grids, Selectors).
Decoupled from dialogs via signals.
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, 
                             QMessageBox, QScrollArea)
from PySide6.QtCore import Signal, Qt

from .primitives.labels import ThemedLabel
from .primitives.containers import ThemedScrollArea
from .items import ProfileItem, TypeItem


class ProfileGrid(QScrollArea):
    """Profile grid with clear separation of UI and functionality"""
    
    # MARK: - Signals
    profile_selected = Signal(str, str)  # (profile_type, profile_name)
    profile_deleted = Signal(str, str)   # (profile_type, profile_name)
    
    # New signals for decoupling
    add_requested = Signal(str)         # (profile_type)
    edit_requested = Signal(str, str)   # (profile_type, profile_name)
    duplicate_requested = Signal(str, str) # (profile_type, profile_name)
    
    def __init__(self, profile_name, parent=None):
        super().__init__(parent)
        
        # MARK: - Properties
        self.profile_name = profile_name  # "hinge" or "lock"
        self.profile_items = {}  # name -> ProfileItem widget
        self.profiles_data = {}  # name -> profile data
        self.selected_profile = None
        
        # MARK: - UI Setup
        self.setup_ui()
        
    # MARK: - UI Setup
    def setup_ui(self):
        """Setup the grid UI"""
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        # Container widget
        container = QWidget()
        container.setObjectName("ProfileGridContainer")
        self.setWidget(container)
        
        # Main layout
        main_layout = QVBoxLayout(container)
        
        # Title
        title = ThemedLabel(f"{self.profile_name.capitalize()} Profiles")
        title.setStyleSheet("""
            QLabel {
                font-size: 16px; 
                font-weight: bold; 
                padding: 10px; 
            }
        """)
        main_layout.addWidget(title)
        
        # Grid layout for items
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(10)
        main_layout.addLayout(self.grid_layout)
        main_layout.addStretch()
        
        # Add initial "+" button
        self.add_plus_button()
    
    def add_plus_button(self):
        """Add the '+' button for creating new profiles"""
        add_item = ProfileItem("Add", is_add_button=True)
        add_item.clicked.connect(self.create_new_profile)
        self.grid_layout.addWidget(add_item, 0, 0)
    
    # MARK: - Update Methods
    def update_profiles(self, profiles_dict, selected_name=None):
        """Update grid with profiles dictionary and selected profile"""
        # Store data
        self.profiles_data = profiles_dict.copy()
        self.selected_profile = selected_name
        
        # Clear existing profile items (keep + button)
        for item in list(self.profile_items.values()):
            item.deleteLater()
        self.profile_items.clear()
        
        # Add profiles
        row, col = 0, 1  # Start after + button
        for profile_name, profile_data in profiles_dict.items():
            self.add_profile_item(profile_name, profile_data, row, col)
            col += 1
            if col > self.get_columns_count():
                col = 0
                row += 1
        
        # Update selection states
        self.update_selection_states()
    
    def add_profile_item(self, name, profile_data, row, col):
        """Add a single profile item to the grid"""
        item = ProfileItem(name, profile_data)
        item.clicked.connect(lambda n: self.on_profile_clicked(n))
        item.edit_requested.connect(self.edit_profile)
        item.duplicate_requested.connect(self.duplicate_profile)
        item.delete_requested.connect(self.delete_profile)
        
        self.profile_items[name] = item
        self.grid_layout.addWidget(item, row, col)
    
    def update_selection_states(self):
        """Update visual selection states of all items"""
        for name, item in self.profile_items.items():
            item.set_selected(name == self.selected_profile)
    
    # MARK: - Event Handlers
    def on_profile_clicked(self, name):
        """Handle profile selection"""
        if name == "Add":
            return
        
        self.selected_profile = name
        self.update_selection_states()
        self.profile_selected.emit(self.profile_name, name)
    
    def create_new_profile(self, _=None):
        """Request new profile creation"""
        self.add_requested.emit(self.profile_name)
    
    def edit_profile(self, name):
        """Request profile edit"""
        self.edit_requested.emit(self.profile_name, name)
    
    def duplicate_profile(self, name):
        """Request profile duplication"""
        self.duplicate_requested.emit(self.profile_name, name)
    
    def delete_profile(self, name):
        """Delete profile after confirmation"""
        reply = QMessageBox.question(self, "Delete Profile", 
                                   f"Are you sure you want to delete '{name}'?",
                                   QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            self.profile_deleted.emit(self.profile_name, name)
    
    # MARK: - Utility Methods
    def get_columns_count(self):
        """Calculate number of columns based on current width"""
        item_width = 130  # ProfileItem width + spacing
        available_width = self.viewport().width()
        return max(1, available_width // item_width)
    
    def resizeEvent(self, event):
        """Handle resize to rearrange grid"""
        super().resizeEvent(event)
        self.rearrange_grid()
    
    def rearrange_grid(self):
        """Rearrange grid items based on current width"""
        columns = self.get_columns_count()
        
        # Get all widgets
        widgets = []
        for i in range(self.grid_layout.count()):
            item = self.grid_layout.itemAt(i)
            if item and item.widget():
                widgets.append(item.widget())
        
        # Clear grid
        while self.grid_layout.count():
            self.grid_layout.takeAt(0)
        
        # Re-add widgets
        row, col = 0, 0
        for widget in widgets:
            self.grid_layout.addWidget(widget, row, col)
            col += 1
            if col >= columns:
                col = 0
                row += 1


class TypeSelector(QWidget):
    """Type selector with selection state preservation"""
    
    # MARK: - Signals
    type_selected = Signal(dict)
    types_modified = Signal()
    
    # Signals for external handling
    add_requested = Signal(str)       # (profile_type)
    edit_requested = Signal(str, str) # (profile_type, type_name)
    duplicate_requested = Signal(str, str) # (profile_type, type_name)
    delete_requested = Signal(str, str) # (profile_type, type_name)
    
    def __init__(self, profile_type, parent=None):
        super().__init__(parent)
        
        # MARK: - Properties
        self.profile_type = profile_type  # "hinge" or "lock"
        self.selected_type_name = None  # Store the name instead of the object
        self.types = {}  # name -> type_data
        self.type_items = {}  # name -> TypeItem widget
        
        # MARK: - UI Setup
        self.setup_ui()
    
    # MARK: - UI Setup
    def setup_ui(self):
        """Setup UI components"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Title
        title = ThemedLabel(f"{self.profile_type.capitalize()} Types")
        title.setStyleSheet("QLabel { font-weight: bold; padding: 5px; }")
        layout.addWidget(title)
        
        # Scroll area
        scroll = ThemedScrollArea()
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setFixedHeight(150)
        scroll.setWidgetResizable(True)
        
        # Container
        container = QWidget()
        container.setObjectName("TypeSelectorContainer")
        self.items_layout = QHBoxLayout(container)
        self.items_layout.setSpacing(10)
        self.items_layout.setContentsMargins(5, 5, 5, 5)
        
        scroll.setWidget(container)
        layout.addWidget(scroll)
        
        # Add initial "+" button
        self.add_type_button()
    
    def add_type_button(self):
        """Add the '+' button"""
        add_item = TypeItem("Add", is_add_button=True)
        add_item.clicked.connect(self.add_new_type)
        self.items_layout.insertWidget(0, add_item)
    
    # MARK: - Data Management
    def load_types(self, types_data):
        """Load types from data and preserve selection"""
        # Remember current selection
        previously_selected = self.selected_type_name
        
        # Clear existing (except add button)
        for item in list(self.type_items.values()):
            item.deleteLater()
        self.type_items.clear()
        self.types.clear()
        
        # Add types
        for type_name, type_data in types_data.items():
            self.add_type_item(type_data)
        
        # Restore selection if the type still exists
        if previously_selected and previously_selected in self.types:
            self.restore_selection(previously_selected)
        else:
            # Clear selection if type no longer exists
            self.selected_type_name = None
    
    def restore_selection(self, type_name):
        """Restore selection to a specific type"""
        if type_name in self.type_items and type_name in self.types:
            self.selected_type_name = type_name
            self.type_items[type_name].set_selected(True)
            # Don't emit signal during restoration
    
    def add_type_item(self, type_data):
        """Add a type item to the selector"""
        name = type_data["name"]
        
        # Create item
        item = TypeItem(name, type_data.get("image"))
        item.clicked.connect(lambda n: self.on_type_clicked(n))
        item.edit_requested.connect(self.edit_type)
        item.duplicate_requested.connect(self.duplicate_type)
        item.delete_requested.connect(self.delete_type)
        
        # Store data and widget
        self.types[name] = type_data
        self.type_items[name] = item
        
        # Add to layout (after the "+" button)
        self.items_layout.addWidget(item)
    
    # MARK: - Event Handlers
    def on_type_clicked(self, name):
        """Handle type selection"""
        # Clear previous selection
        if self.selected_type_name and self.selected_type_name in self.type_items:
            self.type_items[self.selected_type_name].set_selected(False)
        
        # Set new selection
        self.selected_type_name = name
        if name in self.type_items:
            self.type_items[name].set_selected(True)
            self.type_selected.emit(self.types[name])
    
    def add_new_type(self, _=None):
        """Request new type creation"""
        self.add_requested.emit(self.profile_type)
    
    def edit_type(self, name):
        """Request type edit"""
        self.edit_requested.emit(self.profile_type, name)
    
    def duplicate_type(self, name):
        """Request type duplication"""
        self.duplicate_requested.emit(self.profile_type, name)
    
    def delete_type(self, name):
        """Delete type request"""
        # Logic can vary, but usually we confirm here then emit
        reply = QMessageBox.question(self, "Delete Type", 
                                   f"Delete type '{name}'?",
                                   QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            self.delete_requested.emit(self.profile_type, name)
