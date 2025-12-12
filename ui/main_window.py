"""
Main Window for PyPortalMill application
"""

from PySide6.QtWidgets import (QMainWindow, QTabWidget, QMenuBar, QMenu, 
                               QMessageBox)
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt

from core.theme_manager import get_theme_manager
from ui.tabs.profiles_tab import ProfilesTab
from ui.tabs.setup_tab import SetupTab
from ui.tabs.export_tab import ExportTab


class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        self.theme_manager = get_theme_manager()
        self._setup_ui()
        self._create_menu_bar()
        self._connect_signals()
        
        # Set default theme
        self.theme_manager.set_theme("Purple")
        self._apply_theme()
    
    def _setup_ui(self):
        """Setup the main UI"""
        self.setWindowTitle("PyPortalMill")
        self.setMinimumSize(1000, 700)
        
        # Create tab widget
        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)
        
        # Create tabs
        self.profiles_tab = ProfilesTab()
        self.setup_tab = SetupTab()
        self.export_tab = ExportTab()
        
        # Add tabs
        self.tab_widget.addTab(self.profiles_tab, "Profiles")
        self.tab_widget.addTab(self.setup_tab, "Setup")
        self.tab_widget.addTab(self.export_tab, "Export")
    
    def _create_menu_bar(self):
        """Create the menu bar"""
        menubar = self.menuBar()
        
        # View menu
        view_menu = menubar.addMenu("View")
        
        # Select Theme submenu
        select_theme_menu = view_menu.addMenu("Select Theme")
        
        # Default themes
        default_theme_names = self.theme_manager.get_default_theme_names()
        for theme_name in default_theme_names:
            action = QAction(theme_name, self)
            action.triggered.connect(lambda checked, name=theme_name: self._on_theme_selected(name))
            select_theme_menu.addAction(action)
        
        # Separator
        # Separator for user themes (start of user themes)
        select_theme_menu.addSeparator()
        
        # Separator before Theme Editor (end of user themes)
        self.theme_editor_separator = select_theme_menu.addSeparator()
        
        # Theme Editor option
        theme_editor_action = QAction("Theme Editor...", self)
        theme_editor_action.triggered.connect(self._open_theme_editor)
        select_theme_menu.addAction(theme_editor_action)
        
        # Store reference to menu for updates
        self.select_theme_menu = select_theme_menu
        
        # Populate user themes initially
        self.user_themes_actions = []
        self._update_user_themes_menu(select_theme_menu)
    
    def _update_user_themes_menu(self, menu):
        """Update user themes in the menu"""
        # Remove old user theme actions
        for action in self.user_themes_actions:
            menu.removeAction(action)
        self.user_themes_actions.clear()
        
        # Add current user themes
        user_theme_names = self.theme_manager.get_user_theme_names()
        for theme_name in user_theme_names:
            action = QAction(theme_name, self)
            action.triggered.connect(lambda checked, name=theme_name: self._on_theme_selected(name))
            # Insert before the theme editor separator
            menu.insertAction(self.theme_editor_separator, action)
            self.user_themes_actions.append(action)
    
    def _connect_signals(self):
        """Connect signals and slots"""
        self.theme_manager.theme_changed.connect(self._apply_theme)
    
    def _on_theme_selected(self, theme_name: str):
        """Handle theme selection from menu"""
        self.theme_manager.set_theme(theme_name)
    
    def _apply_theme(self):
        """Apply the current theme to the application"""
        stylesheet = self.theme_manager.get_stylesheet()
        self.setStyleSheet(stylesheet)
    
    def _open_theme_editor(self):
        """Open the theme editor dialog"""
        # Import here to avoid circular imports
        from theme_editor.selection_dialog import ThemeSelectionDialog
        
        dialog = ThemeSelectionDialog(self)
        result = dialog.exec()
        
        # Update menu after dialog closes in case themes were added/deleted
        if result:
            self._update_user_themes_menu(self.select_theme_menu)
