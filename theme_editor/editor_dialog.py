"""
Theme Editor Dialog - Main dialog for editing themes
"""

import copy
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QTabWidget,
                               QPushButton, QLabel, QLineEdit, QMessageBox,
                               QComboBox, QFormLayout, QSplitter, QTreeWidget, 
                               QTreeWidgetItem, QStackedWidget)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QColor

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
        self.setMinimumSize(1200, 800)
        
        layout = QVBoxLayout(self)
        
        # Top Bar: Name & Actions
        top_layout = QHBoxLayout()
        name_layout = QFormLayout()
        self.theme_name_input = QLineEdit()
        if self.mode == 'edit':
            self.theme_name_input.setText(self.original_theme_name)
        name_layout.addRow("Theme Name:", self.theme_name_input)
        top_layout.addLayout(name_layout)
        
        top_layout.addStretch()
        
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self._on_cancel)
        top_layout.addWidget(self.cancel_btn)
        
        from widgets.primitives.buttons import GreenButton
        self.confirm_btn = GreenButton("Save Theme")
        self.confirm_btn.clicked.connect(self._save_theme)
        top_layout.addWidget(self.confirm_btn)
        
        layout.addLayout(top_layout)
        
        # --- Main Splitter Content ---
        # from PySide6.QtWidgets import QSplitter, QTreeWidget, QTreeWidgetItem, QStackedWidget
        
        splitter = QSplitter(Qt.Horizontal)
        splitter.setHandleWidth(2)
        splitter.setStyleSheet("QSplitter::handle { background-color: #444; }")
        
        # Left: Navigation
        self.nav_tree = QTreeWidget()
        self.nav_tree.setHeaderHidden(True)
        self.nav_tree.setFixedWidth(200)
        self.nav_tree.itemClicked.connect(self._on_nav_clicked)
        splitter.addWidget(self.nav_tree)
        
        # Right: Content (Stacked Sections)
        self.stack = QStackedWidget()
        splitter.addWidget(self.stack)
        
        # Let stack be wider
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)
        
        layout.addWidget(splitter)
        
        # Register and Load Sections
        self._register_sections()
        self._build_sections()
        
    def _register_sections(self):
        from .registry import ThemeSectionRegistry
        from .sections.global_settings import GlobalSection
        from .sections.buttons import ButtonsSection
        from .sections.inputs import InputsSection
        from .sections.cards import CardsSection
        from .sections.variables import VariablesSection
        from .sections.status_section import StatusSection
        from .sections.editors import EditorsSection
        
        # Clear specific registry if we want to reload, but usually static is fine.
        if not ThemeSectionRegistry.get_sections():
            ThemeSectionRegistry.register("Global", "Colors & Typography", GlobalSection)
            ThemeSectionRegistry.register("Primitives", "Buttons", ButtonsSection)
            ThemeSectionRegistry.register("Primitives", "Inputs", InputsSection)
            ThemeSectionRegistry.register("Primitives", "Variables", VariablesSection)
            ThemeSectionRegistry.register("Components", "Cards", CardsSection)
            ThemeSectionRegistry.register("Components", "Status Cards", StatusSection)
            ThemeSectionRegistry.register("Editors", "G-Code Editor", EditorsSection)
            
    def _build_sections(self):
        from .registry import ThemeSectionRegistry
        
        categories = {} # name -> QTreeWidgetItem
        
        for section_data in ThemeSectionRegistry.get_sections():
            cat = section_data['category']
            name = section_data['name']
            cls = section_data['class']
            
            # Category Item
            if cat not in categories:
                item = QTreeWidgetItem(self.nav_tree, [cat])
                item.setExpanded(True)
                # Style category headers
                item.setFlags(item.flags() & ~Qt.ItemIsSelectable) # Make category not selectable if desired
                # Actually commonly people want to select sub-items.
                item.setForeground(0, QColor("#888"))
                item.setFont(0, QFont("Segoe UI", 9, QFont.Bold))
                categories[cat] = item
            
            # Section Item
            item = QTreeWidgetItem(categories[cat], [name])
            
            # Instantiate Section
            widget = cls(self)
            index = self.stack.addWidget(widget)
            
            # Store index in item data
            item.setData(0, Qt.UserRole, index)
            
        # Select first item
        if self.nav_tree.topLevelItemCount() > 0:
            first_cat = self.nav_tree.topLevelItem(0)
            if first_cat.childCount() > 0:
                self.nav_tree.setCurrentItem(first_cat.child(0))
                self.stack.setCurrentIndex(first_cat.child(0).data(0, Qt.UserRole))

    def _on_nav_clicked(self, item, col):
        index = item.data(0, Qt.UserRole)
        if index is not None:
            self.stack.setCurrentIndex(index)

    def _load_theme_data(self):
        """Load theme data based on mode"""
        if self.mode == 'edit':
            self.theme_data = copy.deepcopy(self.theme_manager.get_theme(self.original_theme_name))
        else:
            # Create mode: clone current
            self.theme_data = copy.deepcopy(self.theme_manager.get_theme(self.theme_manager.current_theme_name))
    
    def get_theme_data(self):
        return self.theme_data
    
    def _save_theme(self):
        """Save the theme"""
        theme_name = self.theme_name_input.text().strip()
        if not theme_name:
            QMessageBox.warning(self, "Invalid Name", "Please enter a theme name.")
            return

        # Name checks... (Same as before)
        if theme_name in self.theme_manager.get_default_theme_names():
            QMessageBox.warning(self, "Invalid Name", "Cannot use a default theme name.")
            return

        if self.mode == 'create' or theme_name != self.original_theme_name:
            if theme_name in self.theme_manager.get_user_theme_names():
                 if QMessageBox.question(self, "Exists", "Overwrite?", QMessageBox.Yes|QMessageBox.No) == QMessageBox.No:
                     return
        
        # Update name
        self.theme_data['name'] = theme_name
        
        # Save
        if self.theme_manager.save_user_theme(theme_name, self.theme_data):
            if self.mode == 'edit' and theme_name != self.original_theme_name:
                self.theme_manager.delete_user_theme(self.original_theme_name)
            QMessageBox.information(self, "Success", f"Theme '{theme_name}' saved!")
            self.accept()
        else:
            QMessageBox.warning(self, "Error", "Failed to save theme.")

    def apply_temporary_theme(self):
        if self.theme_data:
            self.theme_manager.current_theme = self.theme_data
            self.theme_manager.theme_changed.emit("__preview__")
            
            # Regenerate stylesheet and apply to the dialog
            new_stylesheet = self.theme_manager.get_stylesheet()
            self.setStyleSheet(new_stylesheet)
            
            # Force Qt to recompute styles
            self.style().unpolish(self)
            self.style().polish(self)
            
    def _on_cancel(self):
        self.theme_manager.set_theme(self.original_active_theme)
        self.reject()
