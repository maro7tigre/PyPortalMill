"""
Theme Selection Dialog - Manages user themes
"""

from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QListWidget,
                               QPushButton, QLabel, QMessageBox, QListWidgetItem)
from PySide6.QtCore import Qt

from core.theme_manager import get_theme_manager


class ThemeSelectionDialog(QDialog):
    """Dialog for managing user themes"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.theme_manager = get_theme_manager()
        self._setup_ui()
        self._load_user_themes()
    
    def _setup_ui(self):
        """Setup the UI"""
        self.setWindowTitle("Theme Editor")
        self.setMinimumSize(500, 400)
        
        layout = QVBoxLayout(self)
        
        # Title
        title_label = QLabel("User-Made Themes")
        title_label.setStyleSheet("font-size: 14pt; font-weight: bold;")
        layout.addWidget(title_label)
        
        # List of user themes
        self.theme_list = QListWidget()
        layout.addWidget(self.theme_list)
        
        # Buttons at the bottom
        button_layout = QHBoxLayout()
        
        self.add_theme_btn = QPushButton("Add Theme")
        self.add_theme_btn.clicked.connect(self._add_theme)
        
        self.close_btn = QPushButton("Close")
        self.close_btn.clicked.connect(self.accept)
        
        button_layout.addWidget(self.add_theme_btn)
        button_layout.addStretch()
        button_layout.addWidget(self.close_btn)
        
        layout.addLayout(button_layout)
    
    def _load_user_themes(self):
        """Load user themes into the list"""
        self.theme_list.clear()
        
        user_themes = self.theme_manager.get_user_theme_names()
        
        if not user_themes:
            # Show message if no user themes
            item = QListWidgetItem("No user themes yet. Click 'Add Theme' to create one.")
            item.setFlags(Qt.ItemIsEnabled)  # Make it non-selectable
            self.theme_list.addItem(item)
        else:
            for theme_name in user_themes:
                self._add_theme_item(theme_name)
    
    def _add_theme_item(self, theme_name: str):
        """Add a theme item with Edit and Delete buttons"""
        # Create custom widget for the item
        item_widget = QHBoxLayout()
        
        # Theme name label
        name_label = QLabel(theme_name)
        name_label.setStyleSheet("font-size: 11pt;")
        item_widget.addWidget(name_label)
        
        item_widget.addStretch()
        
        # Edit button
        edit_btn = QPushButton("Edit")
        edit_btn.setMaximumWidth(80)
        edit_btn.clicked.connect(lambda: self._edit_theme(theme_name))
        item_widget.addWidget(edit_btn)
        
        # Delete button
        delete_btn = QPushButton("Delete")
        delete_btn.setMaximumWidth(80)
        delete_btn.clicked.connect(lambda: self._delete_theme(theme_name))
        item_widget.addWidget(delete_btn)
        
        # Create container widget
        container = QDialog()  # Use QDialog as a container
        container.setLayout(item_widget)
        
        # Add to list
        list_item = QListWidgetItem()
        list_item.setSizeHint(container.sizeHint())
        self.theme_list.addItem(list_item)
        self.theme_list.setItemWidget(list_item, container)
    
    def _add_theme(self):
        """Add a new theme"""
        # Import here to avoid circular imports
        from ui.dialogs.theme_editor_dialog import ThemeEditorDialog
        
        dialog = ThemeEditorDialog(self, mode='create')
        if dialog.exec():
            # Reload list
            self._load_user_themes()
    
    def _edit_theme(self, theme_name: str):
        """Edit an existing theme"""
        # Import here to avoid circular imports
        from ui.dialogs.theme_editor_dialog import ThemeEditorDialog
        
        dialog = ThemeEditorDialog(self, mode='edit', theme_name=theme_name)
        if dialog.exec():
            # Reload list
            self._load_user_themes()
    
    def _delete_theme(self, theme_name: str):
        """Delete a theme"""
        # Confirm deletion
        reply = QMessageBox.question(
            self,
            "Confirm Deletion",
            f"Are you sure you want to delete the theme '{theme_name}'?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            if self.theme_manager.delete_user_theme(theme_name):
                QMessageBox.information(self, "Success", f"Theme '{theme_name}' deleted successfully.")
                self._load_user_themes()
            else:
                QMessageBox.warning(self, "Error", f"Failed to delete theme '{theme_name}'.")
