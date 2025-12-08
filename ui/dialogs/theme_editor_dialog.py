"""
Theme Editor Dialog - Main dialog for editing themes
"""

import copy
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QTabWidget,
                               QPushButton, QLabel, QLineEdit, QMessageBox,
                               QComboBox, QFormLayout)
from PySide6.QtCore import Qt

from core.theme_manager import get_theme_manager


class ThemeEditorDialog(QDialog):
    """Main theme editor dialog"""
    
    def __init__(self, parent=None, mode='create', theme_name=None):
        """
        Initialize theme editor
        
        Args:
            parent: Parent widget
            mode: 'create' for new theme, 'edit' for existing theme
            theme_name: Name of theme to edit (if mode='edit')
        """
        super().__init__(parent)
        self.theme_manager = get_theme_manager()
        self.mode = mode
        self.original_theme_name = theme_name
        self.theme_data = None
        
        # Store the theme that was active when dialog opened (for cancel reversion)
        self.original_active_theme = self.theme_manager.current_theme_name
        
        # Load theme data BEFORE setting up UI so widgets can access it
        self._load_theme_data()
        self._setup_ui()
        
        # Apply temporary theme for live preview
        self.apply_temporary_theme()
    
    def _setup_ui(self):
        """Setup the UI"""
        self.setWindowTitle("Theme Editor" if self.mode == 'create' else f"Edit Theme: {self.original_theme_name}")
        self.setMinimumSize(900, 700)
        
        layout = QVBoxLayout(self)
        
        # Theme name input
        name_layout = QFormLayout()
        self.theme_name_input = QLineEdit()
        if self.mode == 'edit':
            self.theme_name_input.setText(self.original_theme_name)
        name_layout.addRow("Theme Name:", self.theme_name_input)
        layout.addLayout(name_layout)
        
        # Info label for create mode
        if self.mode == 'create':
            info_label = QLabel(f"Creating new theme based on: {self.theme_manager.current_theme_name}")
            info_label.setStyleSheet("font-style: italic; color: #888;")
            layout.addWidget(info_label)
        
        # Tab widget for Colors and Style
        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)
        
        # Import and create tabs
        from ui.dialogs.theme_editor.colors_tab import ColorsTab
        from ui.dialogs.theme_editor.style_tab import StyleTab
        
        self.colors_tab = ColorsTab(self)
        self.style_tab = StyleTab(self)
        
        self.tab_widget.addTab(self.colors_tab, "Colors")
        self.tab_widget.addTab(self.style_tab, "Style")
        
        # Bottom buttons
        button_layout = QHBoxLayout()
        
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self._on_cancel)
        
        self.confirm_btn = QPushButton("Confirm")
        self.confirm_btn.clicked.connect(self._save_theme)
        
        button_layout.addWidget(self.cancel_btn)
        button_layout.addStretch()
        button_layout.addWidget(self.confirm_btn)
        
        layout.addLayout(button_layout)
    
    def _load_theme_data(self):
        """Load theme data based on mode"""
        if self.mode == 'edit':
            # Load existing theme
            self.theme_data = copy.deepcopy(self.theme_manager.get_theme(self.original_theme_name))
        else:
            # Will be loaded when clone selection changes or when dialog is shown
            pass
    
    def get_theme_data(self):
        """Get current theme data (used by tabs)"""
        if self.theme_data is None and self.mode == 'create':
            # Load from currently active theme
            self.theme_data = copy.deepcopy(self.theme_manager.get_theme(self.theme_manager.current_theme_name))
        
        return self.theme_data
    
    def get_style_data(self):
        """Get current style data (used by style tab)"""
        theme_data = self.get_theme_data()
        if theme_data and 'control_styles' in theme_data:
            return copy.deepcopy(theme_data['control_styles'])
        # Return default control styles if none exist
        return {
            "buttons": {"border_radius": 4, "padding_horizontal": 12, "padding_vertical": 6, "font_size": 11, "font_weight": "normal", "border_width": 1},
            "inputs": {"border_radius": 4, "padding_horizontal": 8, "padding_vertical": 4, "font_size": 10, "border_width": 1, "focus_border_width": 2},
            "cards": {"border_radius": 8, "padding": 12, "border_width": 0},
            "labels": {"font_size_primary": 14, "font_size_secondary": 10, "font_weight_primary": "bold", "font_weight_secondary": "normal"}
        }
    
    def _save_theme(self):
        """Save the theme"""
        theme_name = self.theme_name_input.text().strip()
        
        if not theme_name:
            QMessageBox.warning(self, "Invalid Name", "Please enter a theme name.")
            return
        
        # Check if name conflicts with default themes
        if theme_name in self.theme_manager.get_default_theme_names():
            QMessageBox.warning(self, "Invalid Name", 
                              "Cannot use a default theme name. Please choose a different name.")
            return
        
        # Check if name conflicts with other user themes (except when editing the same theme)
        if self.mode == 'create' or theme_name != self.original_theme_name:
            if theme_name in self.theme_manager.get_user_theme_names():
                reply = QMessageBox.question(
                    self,
                    "Theme Exists",
                    f"A theme named '{theme_name}' already exists. Do you want to overwrite it?",
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.No
                )
                if reply == QMessageBox.No:
                    return
        
        # Get theme data from colors tab
        theme_data = self.colors_tab.get_theme_data()
        theme_data['name'] = theme_name
        
        # Get style data from style tab and include in theme
        style_data = self.style_tab.get_style_data()
        theme_data['control_styles'] = style_data
        
        # Save theme
        if self.theme_manager.save_user_theme(theme_name, theme_data):
            # If editing and name changed, delete old theme
            if self.mode == 'edit' and theme_name != self.original_theme_name:
                self.theme_manager.delete_user_theme(self.original_theme_name)
            
            QMessageBox.information(self, "Success", f"Theme '{theme_name}' saved successfully!")
            self.accept()
        else:
            QMessageBox.warning(self, "Error", "Failed to save theme.")
    
    def apply_temporary_theme(self):
        """Apply the current editing theme as a temporary theme for live preview"""
        if self.theme_data:
            # Temporarily replace current theme
            self.theme_manager.current_theme = self.theme_data
            self.theme_manager.theme_changed.emit("__preview__")
    
    def _on_cancel(self):
        """Handle cancel - revert to original theme"""
        # Revert to the theme that was active when dialog opened
        self.theme_manager.set_theme(self.original_active_theme)
        self.reject()
