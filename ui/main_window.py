"""
Main Window for PyPortalMill application
"""

from PySide6.QtWidgets import (QMainWindow, QTabWidget, QMenuBar, QMenu, 
                                QMessageBox)
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt

from core.theme_manager import get_theme_manager


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
        self.setWindowTitle("PyPortalMill - Wizard System")
        self.setMinimumSize(1200, 800)
        
        # Create main tab widget with vertical tabs on the left
        self.main_tabs = QTabWidget()
        self.main_tabs.setTabPosition(QTabWidget.West)  # Tabs on left side
        self.setCentralWidget(self.main_tabs)
        
        # Create dynamic tabs from config
        from core.config_manager import get_config_manager
        from ui.tabs.generic_wizard_tab import GenericWizardTab
        
        config_manager = get_config_manager()
        self.wizard_tabs = []
        
        for tab_config in config_manager.get_tabs():
            tab = GenericWizardTab(tab_config)
            self.main_tabs.addTab(tab, tab_config.name)
            self.wizard_tabs.append(tab)
            
        # Fallback if config is empty (just for safety during dev)
        if not self.wizard_tabs:
            print("WARNING: No tabs found in config! Check settings.json")

    
    def _create_menu_bar(self):
        """Create the menu bar"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("File")
        
        # Project actions
        save_project_action = QAction("Save Project", self)
        save_project_action.setShortcut("Ctrl+S")
        save_project_action.triggered.connect(self._save_project)
        file_menu.addAction(save_project_action)
        
        load_project_action = QAction("Load Project", self)
        load_project_action.setShortcut("Ctrl+O")
        load_project_action.triggered.connect(self._load_project)
        file_menu.addAction(load_project_action)
        
        file_menu.addSeparator()
        
        # Set actions
        save_set_action = QAction("Save Profile Set", self)
        save_set_action.triggered.connect(self._save_set)
        file_menu.addAction(save_set_action)
        
        load_set_action = QAction("Load Profile Set", self)
        load_set_action.triggered.connect(self._load_set)
        file_menu.addAction(load_set_action)
        
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
        
        # Configuration menu
        config_menu = menubar.addMenu("Configuration")
        
        # Select Config submenu
        select_config_menu = config_menu.addMenu("Select Configuration")
        
        # Separator for user configs
        self.config_editor_separator = select_config_menu.addSeparator()
        
        # Config Editor option
        config_editor_action = QAction("Config Editor...", self)
        config_editor_action.triggered.connect(self._open_config_editor)
        select_config_menu.addAction(config_editor_action)
        
        # Store reference for updates
        self.select_config_menu = select_config_menu
        self.config_actions = []
        
        # Populate configs
        self._update_config_menu()

    def _update_config_menu(self):
        """Update configurations in the menu"""
        # Remove old actions
        for action in self.config_actions:
            self.select_config_menu.removeAction(action)
        self.config_actions.clear()
        
        # Add available configs
        from core.config_manager import get_config_manager
        cm = get_config_manager()
        
        for config_name in cm.get_available_configs():
            action = QAction(config_name, self)
            action.setCheckable(True)
            action.setChecked(config_name == cm.current_config_name)
            action.triggered.connect(lambda checked, name=config_name: self._on_config_selected(name))
            
            # Insert before separator
            self.select_config_menu.insertAction(self.config_editor_separator, action)
            self.config_actions.append(action)

    def _on_config_selected(self, config_name: str):
        """Handle config selection"""
        from core.config_manager import get_config_manager
        cm = get_config_manager()
        if cm.set_config(config_name):
            self._update_config_menu() # Update checkmarks

    def _open_config_editor(self):
        """Open config editor dialog"""
        from ui.dialogs.config_editor_dialog import ConfigEditorDialog
        from core.config_manager import get_config_manager
        
        # Simple selection dialog or direct open?
        # For now, let's open the editor with "Select/Create" mode or just list valid configs.
        # Implemented similar to Theme Editor logic where you select what to edit in the dialog or passed in.
        # But ConfigEditorDialog currently takes a specific config.
        # Let's create a wrapper or simple selection input first?
        # Actually, let's just default to editing the CURRENT config, and inside the dialog allow switching/creating?
        # The current ConfigEditorDialog takes (parent, mode, name). 
        # Let's allow picking a config to edit via a small intermediate dialog OR
        # just open a selection dialog similar to ThemeSelectionDialog. 
        # For MVP, let's open a selection dialog first.
        
        # Let's create a quick ConfigSelectionDialog similar to ThemeSelectionDialog
        from ui.dialogs.config_selection_dialog import ConfigSelectionDialog
        dialog = ConfigSelectionDialog(self)
        if dialog.exec():
            self._update_config_menu()

    def _connect_signals(self):
        """Connect signals and slots"""
        self.theme_manager.theme_changed.connect(self._apply_theme)
        
        # Connect config changed signal to reload tabs
        from core.config_manager import get_config_manager
        get_config_manager().config_changed.connect(self._on_config_changed)
    
    def _on_config_changed(self, config_name: str):
        """Handle configuration changes"""
        # Re-create tabs
        self.main_tabs.clear()
        self.wizard_tabs = []
        
        from core.config_manager import get_config_manager
        from ui.tabs.generic_wizard_tab import GenericWizardTab
        
        config_manager = get_config_manager()
        for tab_config in config_manager.get_tabs():
            tab = GenericWizardTab(tab_config)
            self.main_tabs.addTab(tab, tab_config.name)
            self.wizard_tabs.append(tab)
            
        self._update_config_menu() # Ensure menu is in sync
    
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
        from ui.dialogs.theme_selection_dialog import ThemeSelectionDialog
        
        dialog = ThemeSelectionDialog(self)
        result = dialog.exec()
        
        # Update menu after dialog closes in case themes were added/deleted
        if result:
            self._update_user_themes_menu(self.select_theme_menu)
    
    def _save_project(self):
        """Save current project (both doors and frames)"""
        # TODO: Implement project saving
        QMessageBox.information(self, "Save Project", "Project save functionality to be implemented")
    
    def _load_project(self):
        """Load a project (both doors and frames)"""
        # TODO: Implement project loading
        QMessageBox.information(self, "Load Project", "Project load functionality to be implemented")
    
    def _save_set(self):
        """Save current profile set"""
        # TODO: Implement profile set saving
        QMessageBox.information(self, "Save Set", "Profile set save functionality to be implemented")
    
    def _load_set(self):
        """Load a profile set"""
        # TODO: Implement profile set loading
        QMessageBox.information(self, "Load Set", "Profile set load functionality to be implemented")

