"""
Config Selection Dialog
Allows selecting a configuration to edit, creating a new one, or deleting user configs.
"""

from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton, 
                               QLabel, QListWidget, QMessageBox)
from core.config_manager import get_config_manager
from ui.dialogs.config_editor_dialog import ConfigEditorDialog

class ConfigSelectionDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.config_manager = get_config_manager()
        self.setWindowTitle("Select Configuration to Edit")
        self.resize(400, 300)
        
        self._setup_ui()
        
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        
        # List of configs
        layout.addWidget(QLabel("Available Configurations:"))
        self.config_list = QListWidget()
        layout.addWidget(self.config_list)
        
        self.populate_list()
        
        # Buttons
        btn_layout = QHBoxLayout()
        
        self.new_btn = QPushButton("New Config")
        self.new_btn.clicked.connect(self._create_new)
        
        self.edit_btn = QPushButton("Edit Selected")
        self.edit_btn.clicked.connect(self._edit_selected)
        
        self.delete_btn = QPushButton("Delete Selected")
        self.delete_btn.clicked.connect(self._delete_selected)
        
        btn_layout.addWidget(self.new_btn)
        btn_layout.addWidget(self.edit_btn)
        btn_layout.addWidget(self.delete_btn)
        
        layout.addLayout(btn_layout)
        
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)

    def populate_list(self):
        self.config_list.clear()
        configs = self.config_manager.get_available_configs()
        # Sort so Default is first
        if "Default" in configs:
            configs.remove("Default")
            configs.insert(0, "Default")
            
        for name in configs:
            self.config_list.addItem(name)
            
    def _create_new(self):
        # Create new config based on current active one
        dialog = ConfigEditorDialog(self, mode='create')
        if dialog.exec():
            self.populate_list()
            
    def _edit_selected(self):
        item = self.config_list.currentItem()
        if not item:
            return
            
        config_name = item.text()
        
        # If default, warn it's read only or open in view-only/copy mode?
        # Theme editor opens it but saving forces a new name if it's default.
        # ConfigEditorDialog handles creating a copy if needed or blocking overwrite of default.
        
        mode = 'edit'
        if config_name == "Default":
             # We can treat editing default as "create new based on default" or just open read-only
             # For now, let's just open it, the editor prevents saving as "Default"
             pass

        dialog = ConfigEditorDialog(self, mode=mode, config_name=config_name)
        if dialog.exec():
            self.populate_list()
            
    def _delete_selected(self):
        item = self.config_list.currentItem()
        if not item:
            return
            
        config_name = item.text()
        if config_name == "Default":
            QMessageBox.warning(self, "Error", "Cannot delete Default configuration.")
            return
            
        reply = QMessageBox.question(self, "Delete Config", 
                                     f"Are you sure you want to delete '{config_name}'?",
                                     QMessageBox.Yes | QMessageBox.No)
                                     
        if reply == QMessageBox.Yes:
            if self.config_manager.delete_user_config(config_name):
                self.populate_list()
            else:
                QMessageBox.warning(self, "Error", "Failed to delete configuration.")
