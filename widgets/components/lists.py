from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, 
                             QMessageBox, QListWidget)
from PySide6.QtCore import Signal, Qt

from ..primitives.labels import ThemedLabel
from ..primitives.containers import ThemedScrollArea
from widgets.mixins import ThemedWidgetMixin
from .cards import ProfileItem, TypeItem

class ThemedListWidget(QListWidget, ThemedWidgetMixin):
    """Simple themed list"""
    def __init__(self, parent=None):
        super().__init__(parent)
        ThemedWidgetMixin.__init__(self)

class ProfileGrid(ThemedScrollArea):
    """Profile grid with refactored logic"""
    profile_selected = Signal(str, str)
    profile_deleted = Signal(str, str)
    add_requested = Signal(str)
    edit_requested = Signal(str, str)
    duplicate_requested = Signal(str, str)
    
    def __init__(self, profile_name, parent=None):
        super().__init__(parent)
        self.profile_name = profile_name
        self.profile_items = {}
        self.profiles_data = {}
        self.selected_profile = None
        self.setup_ui()
        
    def setup_ui(self):
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        container = QWidget()
        # Theme handling for container background is tricky if not in stylesheet
        # But ThemedScrollArea background should cover it if container is transparent? 
        # No, container needs to be transparent or match specific bg.
        container.setAttribute(Qt.WA_StyledBackground, True)
        container.setStyleSheet("background-color: transparent;") 
        self.setWidget(container)
        
        main_layout = QVBoxLayout(container)
        
        title = ThemedLabel(f"{self.profile_name.capitalize()} Profiles")
        title.setStyleSheet("font-size: 16px; font-weight: bold; padding: 10px;")
        main_layout.addWidget(title)
        
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(10)
        main_layout.addLayout(self.grid_layout)
        main_layout.addStretch()
        
        self.add_plus_button()
        
    def add_plus_button(self):
        add_item = ProfileItem("Add", is_add_button=True)
        add_item.clicked.connect(self.create_new_profile)
        self.grid_layout.addWidget(add_item, 0, 0)
        
    def update_profiles(self, profiles_dict, selected_name=None):
        self.profiles_data = profiles_dict.copy()
        self.selected_profile = selected_name
        
        for item in list(self.profile_items.values()):
            item.deleteLater()
        self.profile_items.clear()
        
        row, col = 0, 1
        for profile_name, profile_data in profiles_dict.items():
            self.add_profile_item(profile_name, profile_data, row, col)
            col += 1
            if col > self.get_columns_count():
                col = 0
                row += 1
        self.update_selection_states()
        
    def add_profile_item(self, name, profile_data, row, col):
        item = ProfileItem(name, profile_data)
        item.clicked.connect(lambda n: self.on_profile_clicked(n))
        item.edit_requested.connect(self.edit_profile)
        item.duplicate_requested.connect(self.duplicate_profile)
        item.delete_requested.connect(self.delete_profile)
        self.profile_items[name] = item
        self.grid_layout.addWidget(item, row, col)
        
    def update_selection_states(self):
        for name, item in self.profile_items.items():
            item.set_selected(name == self.selected_profile)
            
    def on_profile_clicked(self, name):
        if name == "Add": return
        self.selected_profile = name
        self.update_selection_states()
        self.profile_selected.emit(self.profile_name, name)
        
    def create_new_profile(self, _=None): self.add_requested.emit(self.profile_name)
    def edit_profile(self, name): self.edit_requested.emit(self.profile_name, name)
    def duplicate_profile(self, name): self.duplicate_requested.emit(self.profile_name, name)
    def delete_profile(self, name):
        reply = QMessageBox.question(self, "Delete Profile", f"Are you sure you want to delete '{name}'?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes: self.profile_deleted.emit(self.profile_name, name)
        
    def get_columns_count(self):
        return max(1, self.viewport().width() // 130)
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.rearrange_grid()
    def rearrange_grid(self):
        columns = self.get_columns_count()
        widgets = []
        for i in range(self.grid_layout.count()):
            item = self.grid_layout.itemAt(i)
            if item and item.widget(): widgets.append(item.widget())
        while self.grid_layout.count(): self.grid_layout.takeAt(0)
        row, col = 0, 0
        for widget in widgets:
            self.grid_layout.addWidget(widget, row, col)
            col += 1
            if col >= columns: col = 0; row += 1

class TypeSelector(QWidget, ThemedWidgetMixin):
    """Type selector with selection state preservation"""
    type_selected = Signal(dict)
    types_modified = Signal()
    add_requested = Signal(str)
    edit_requested = Signal(str, str)
    duplicate_requested = Signal(str, str)
    delete_requested = Signal(str, str)
    
    def __init__(self, profile_type, parent=None):
        super().__init__(parent)
        ThemedWidgetMixin.__init__(self)
        self.profile_type = profile_type
        self.selected_type_name = None
        self.types = {}
        self.type_items = {}
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        title = ThemedLabel(f"{self.profile_type.capitalize()} Types")
        title.setStyleSheet("font-weight: bold; padding: 5px;")
        layout.addWidget(title)
        
        scroll = ThemedScrollArea()
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setFixedHeight(150)
        scroll.setWidgetResizable(True)
        
        container = QWidget()
        container.setAttribute(Qt.WA_StyledBackground, True)
        container.setStyleSheet("background-color: transparent;") # Rely on scroll area bg
        self.items_layout = QHBoxLayout(container)
        self.items_layout.setSpacing(10)
        self.items_layout.setContentsMargins(5, 5, 5, 5)
        
        scroll.setWidget(container)
        layout.addWidget(scroll)
        
        self.add_type_button()
        
    def add_type_button(self):
        add_item = TypeItem("Add", is_add_button=True)
        add_item.clicked.connect(self.add_new_type)
        self.items_layout.insertWidget(0, add_item)
        
    def load_types(self, types_data):
        previously_selected = self.selected_type_name
        for item in list(self.type_items.values()): item.deleteLater()
        self.type_items.clear()
        self.types.clear()
        for type_name, type_data in types_data.items(): self.add_type_item(type_data)
        if previously_selected and previously_selected in self.types: self.restore_selection(previously_selected)
        else: self.selected_type_name = None
        
    def restore_selection(self, type_name):
        if type_name in self.type_items:
            self.selected_type_name = type_name
            self.type_items[type_name].set_selected(True)
            
    def add_type_item(self, type_data):
        name = type_data["name"]
        item = TypeItem(name, type_data.get("image"))
        item.clicked.connect(lambda n: self.on_type_clicked(n))
        item.edit_requested.connect(self.edit_type)
        item.duplicate_requested.connect(self.duplicate_type)
        item.delete_requested.connect(self.delete_type)
        self.types[name] = type_data
        self.type_items[name] = item
        self.items_layout.addWidget(item)
        
    def on_type_clicked(self, name):
        if self.selected_type_name and self.selected_type_name in self.type_items:
            self.type_items[self.selected_type_name].set_selected(False)
        self.selected_type_name = name
        if name in self.type_items:
            self.type_items[name].set_selected(True)
            self.type_selected.emit(self.types[name])
            
    def add_new_type(self, _=None): self.add_requested.emit(self.profile_type)
    def edit_type(self, name): self.edit_requested.emit(self.profile_type, name)
    def duplicate_type(self, name): self.duplicate_requested.emit(self.profile_type, name)
    def delete_type(self, name):
        reply = QMessageBox.question(self, "Delete Type", f"Delete type '{name}'?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes: self.delete_requested.emit(self.profile_type, name)
