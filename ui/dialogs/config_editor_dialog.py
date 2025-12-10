"""
Config Editor Dialog
GUI-based editor for configuration management.
"""

import copy
import json
from dataclasses import asdict
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton, 
                               QLabel, QLineEdit, QMessageBox, QComboBox, 
                               QTreeWidget, QTreeWidgetItem, QSplitter, QTreeWidgetItemIterator,
                               QWidget, QListWidget, QTabWidget, QToolBar, QMenu)
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QIcon

from core.config_manager import (get_config_manager, TabConfig, ProfileConfig, 
                                 ParameterSectionConfig, ParameterConfig, GroupedAutoConfig)
from ui.dialogs.config_editor.config_editor_widgets import DraggableTreeWidget, PropertiesEditor

class ConfigEditorDialog(QDialog):
    """Main config editor dialog"""
    
    def __init__(self, parent=None, mode='create', config_name=None):
        super().__init__(parent)
        self.config_manager = get_config_manager()
        self.mode = mode
        self.original_config_name = config_name
        self.original_active_config = self.config_manager.current_config_name
        
        self.setWindowTitle("Config Editor" if mode == 'create' else f"Edit Config: {config_name}")
        self.setMinimumSize(1200, 800)
        
        self._load_data()
        self._setup_ui()
        
    def _load_data(self):
        # We work on a deep copy of the configuration data structure (List[TabConfig])
        # ConfigManager gives us TabConfig objects, we need to clone them to avoid live edits
        
        raw_data = None
        if self.mode == 'edit' and self.original_config_name:
             raw_data = self.config_manager.get_config_data(self.original_config_name)
        else:
             raw_data = self.config_manager.get_config_data(self.config_manager.current_config_name)
             
        # Manually reconstruct objects from raw dicts to ensure we have clean objects
        # This mirrors _parse_current_config but for our local copy
        self.tabs = []
        if raw_data:
            for tab_data in raw_data.get("tabs", []):
                # ... same parsing logic as ConfigManager or just use deepcopy if possible ...
                # Since ConfigManager stores objects in self.tabs but only exposes data via get_config_data (raw dict),
                # we should re-parse using the helper logic or just rely on raw dicts and map back?
                # Ideally, we used the objects. 
                # Let's clone the parsing logic briefly or assume we can use the manager to parse a dummy config?
                # Actually, self.config_manager.get_tabs() returns live objects of current config.
                # Since we accept raw dicts to save, we should working with OBJECTS in the UI and serialize to DICT on save.
                
                # Let's Implement a mini-parser here or reuse ConfigManager's logic if refactored.
                # For expedience, I will implement a quick object builder.
                
                profiles = [ProfileConfig(**p) for p in tab_data.get("profiles", [])]
                sections = []
                for s in tab_data.get("parameter_sections", []):
                    params = []
                    for p in s.get("parameters", []):
                        # Handle key mapping from JSON (min/max) to Object (min_value/max_value)
                        p_copy = p.copy()
                        if "min" in p_copy:
                            p_copy["min_value"] = p_copy.pop("min")
                        if "max" in p_copy:
                            p_copy["max_value"] = p_copy.pop("max")
                        params.append(ParameterConfig(**p_copy))
                    
                    ga = None
                    if s.get("grouped_auto"):
                        ga = GroupedAutoConfig(**s.get("grouped_auto"))
                    sections.append(ParameterSectionConfig(
                        id=s.get("id"), title=s.get("title", ""), position=s.get("position", "left"),
                        parameters=params, grouped_auto=ga
                    ))
                self.tabs.append(TabConfig(
                    id=tab_data.get("id"), name=tab_data.get("name"), 
                    profiles=profiles, parameter_sections=sections,
                    profile_validation=tab_data.get("profile_validation", "none")
                ))

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        
        # Name Input
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("Config Name:"))
        self.name_input = QLineEdit()
        if self.mode == 'edit':
            self.name_input.setText(self.original_config_name)
        elif self.mode == 'create':
             self.name_input.setText(f"{self.config_manager.current_config_name}_copy")
        name_layout.addWidget(self.name_input)
        main_layout.addLayout(name_layout)
        
        # 3-Pane Layout
        splitter = QSplitter(Qt.Horizontal)
        
        # Pane 1: Tab List
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.addWidget(QLabel("Tabs"))
        self.tab_list = QListWidget()
        self.tab_list.currentRowChanged.connect(self._on_tab_selected)
        left_layout.addWidget(self.tab_list)
        
        # Tab Control Buttons
        tab_btn_layout = QHBoxLayout()
        add_tab_btn = QPushButton("+")
        add_tab_btn.clicked.connect(self._add_tab)
        del_tab_btn = QPushButton("-")
        del_tab_btn.clicked.connect(self._del_tab)
        tab_btn_layout.addWidget(add_tab_btn)
        tab_btn_layout.addWidget(del_tab_btn)
        left_layout.addLayout(tab_btn_layout)
        
        splitter.addWidget(left_widget)
        
        # Pane 2: Workspace (Center)
        center_widget = QWidget()
        center_layout = QVBoxLayout(center_widget)
        
        self.workspace_tabs = QTabWidget()
        self.workspace_tabs.currentChanged.connect(self._rebuild_workspace) # Refresh on switch?
        
        # Profile Sub-Tab
        self.profile_widget = QWidget()
        profile_layout = QVBoxLayout(self.profile_widget)
        
        # Profile Toolbar
        profile_toolbar = QHBoxLayout()
        add_profile_btn = QPushButton("Add Profile")
        add_profile_btn.clicked.connect(self._add_profile)
        del_profile_btn = QPushButton("Remove Profile")
        del_profile_btn.clicked.connect(self._del_profile)
        profile_toolbar.addWidget(add_profile_btn)
        profile_toolbar.addWidget(del_profile_btn)
        profile_layout.addLayout(profile_toolbar)
        
        self.profile_list = QListWidget()
        self.profile_list.itemClicked.connect(self._on_profile_selected)
        profile_layout.addWidget(self.profile_list)
        
        self.workspace_tabs.addTab(self.profile_widget, "Profiles")
        
        # Layout Sub-Tab
        self.layout_widget = QWidget()
        layout_layout = QVBoxLayout(self.layout_widget)
        
        # Layout Toolbar
        layout_toolbar = QHBoxLayout()
        add_section_btn = QPushButton("Add Section")
        add_section_btn.clicked.connect(self._add_section)
        add_param_btn = QPushButton("Add Parameter")
        add_param_btn.clicked.connect(self._add_parameter)
        del_item_btn = QPushButton("Remove Item")
        del_item_btn.clicked.connect(self._del_layout_item)
        layout_toolbar.addWidget(add_section_btn)
        layout_toolbar.addWidget(add_param_btn)
        layout_toolbar.addWidget(del_item_btn)
        layout_layout.addLayout(layout_toolbar)
        
        # Two Columns for Layout
        columns_splitter = QSplitter(Qt.Horizontal)
        
        self.left_tree = DraggableTreeWidget()
        self.left_tree.itemClicked.connect(self._on_tree_item_selected)
        self.left_tree.drop_requested.connect(lambda t, p: self._handle_drop(self.left_tree, t, p))
        
        self.right_tree = DraggableTreeWidget()
        self.right_tree.itemClicked.connect(self._on_tree_item_selected)
        self.right_tree.drop_requested.connect(lambda t, p: self._handle_drop(self.right_tree, t, p))
        
        columns_splitter.addWidget(self.left_tree)
        columns_splitter.addWidget(self.right_tree)
        layout_layout.addWidget(columns_splitter)
        
        self._setup_selection_logic()
        
        self.workspace_tabs.addTab(self.layout_widget, "Layout")
        
        center_layout.addWidget(self.workspace_tabs)
        splitter.addWidget(center_widget)
        
        # Pane 3: Properties (Right)
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.addWidget(QLabel("Properties"))
        
        self.properties_editor = PropertiesEditor()
        self.properties_editor.data_changed.connect(self._refresh_ui)
        right_layout.addWidget(self.properties_editor)
        
        splitter.addWidget(right_widget)
        
        # Set splitter sizes
        splitter.setSizes([200, 600, 300])
        main_layout.addWidget(splitter)
        
        # Footer Buttons
        btn_layout = QHBoxLayout()
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self._save)
        btn_layout.addWidget(cancel_btn)
        btn_layout.addStretch()
        btn_layout.addWidget(save_btn)
        main_layout.addLayout(btn_layout)
        
        # Initial Population
        self._populate_tabs()
        
    def _populate_tabs(self):
        self.tab_list.clear()
        for tab in self.tabs:
            self.tab_list.addItem(tab.name)
            
        if self.tabs:
            self.tab_list.setCurrentRow(0)

    def _get_current_tab(self):
        row = self.tab_list.currentRow()
        if row >= 0 and row < len(self.tabs):
            return self.tabs[row]
        return None

    def _on_tab_selected(self):
        tab = self._get_current_tab()
        if tab:
            self._rebuild_workspace()
            self.properties_editor.edit_object(tab, "tab")

    def _rebuild_workspace(self):
        tab = self._get_current_tab()
        if not tab: return
        
        # Profiles
        self.profile_list.clear()
        for p in tab.profiles:
             self.profile_list.addItem(p.name)
             
        # Layout Trees
        self.left_tree.clear()
        self.right_tree.clear()
        
        for section in tab.parameter_sections:
            root = QTreeWidgetItem([section.title])
            root.setData(0, Qt.UserRole, "section")
            root.setData(0, Qt.UserRole + 1, section) # Store object
            
            for param in section.parameters:
                child = QTreeWidgetItem([param.name])
                child.setData(0, Qt.UserRole, "parameter")
                child.setData(0, Qt.UserRole + 1, param)
                root.addChild(child)
                
            root.setExpanded(True)
            if section.position == "left":
                self.left_tree.addTopLevelItem(root)
            else:
                self.right_tree.addTopLevelItem(root)

    def _on_profile_selected(self, item):
        tab = self._get_current_tab()
        row = self.profile_list.row(item)
        if tab and row >= 0:
            profile = tab.profiles[row]
            self.properties_editor.edit_object(profile, "profile")

    def _on_tree_item_selected(self, item, column):
        obj = item.data(0, Qt.UserRole + 1)
        role = item.data(0, Qt.UserRole)
        self.properties_editor.edit_object(obj, role)

    def _refresh_ui(self):
        # Called when properties change, refresh lists (e.g. name update)
        # Note: Ideally we update only the changed item
        tab = self._get_current_tab()
        if not tab: return
        
        # Update Tab Name in list
        if self.tab_list.currentItem().text() != tab.name:
             self.tab_list.currentItem().setText(tab.name)
             
        # Update Profile List Names
        for i in range(self.profile_list.count()):
            self.profile_list.item(i).setText(tab.profiles[i].name)
            
        # Update Tree Names
        # Recursive update or just rebuild? Rebuild is easier but resets expansion.
        # Let's simple traverse and update text
        for tree in [self.left_tree, self.right_tree]:
            iterator = QTreeWidgetItemIterator(tree)
            while iterator.value():
                item = iterator.value()
                obj = item.data(0, Qt.UserRole + 1)
                if hasattr(obj, 'title'): item.setText(0, obj.title)
                elif hasattr(obj, 'name'): item.setText(0, obj.name)
                iterator += 1


    def _add_tab(self):
        new_tab = TabConfig(id=f"tab_{len(self.tabs)+1}", name="New Tab", profiles=[], parameter_sections=[])
        self.tabs.append(new_tab)
        self._populate_tabs()
        self.tab_list.setCurrentRow(len(self.tabs)-1)
        
    def _del_tab(self):
        row = self.tab_list.currentRow()
        if row >= 0:
            del self.tabs[row]
            self._populate_tabs()
            
    def _add_profile(self):
        tab = self._get_current_tab()
        if tab:
            new_p = ProfileConfig(id=f"p_{len(tab.profiles)+1}", name="New Profile", type="hardware")
            tab.profiles.append(new_p)
            self._rebuild_workspace()
            
    def _del_profile(self):
        tab = self._get_current_tab()
        row = self.profile_list.currentRow()
        if tab and row >= 0:
            del tab.profiles[row]
            self._rebuild_workspace()

    def _setup_selection_logic(self):
        # Enforce exclusive selection between trees
        self.left_tree.itemPressed.connect(lambda: self.right_tree.clearSelection())
        self.left_tree.itemPressed.connect(lambda: self.right_tree.setCurrentItem(None))
        
        self.right_tree.itemPressed.connect(lambda: self.left_tree.clearSelection())
        self.right_tree.itemPressed.connect(lambda: self.left_tree.setCurrentItem(None))

    def _add_section(self):
        tab = self._get_current_tab()
        if not tab: return
        
        # Decide which tree is active or default to Left
        pos = "left"
        if self.right_tree.selectedItems(): pos = "right"
        
        new_sec = ParameterSectionConfig(id=f"sec_{len(tab.parameter_sections)+1}", title="New Section", position=pos, parameters=[])
        tab.parameter_sections.append(new_sec)
        self._rebuild_workspace()
        
    def _add_parameter(self):
        # Find active tree
        tree = None
        if self.left_tree.selectedItems(): tree = self.left_tree
        elif self.right_tree.selectedItems(): tree = self.right_tree
        
        if not tree: return
        
        item = tree.currentItem()
        if not item: return
        
        # Must select a section
        parent = item if item.data(0, Qt.UserRole) == "section" else item.parent()
        if not parent: return
        
        section = parent.data(0, Qt.UserRole + 1)
        new_param = ParameterConfig(name="new_param", label="New Parameter", type="string", default="")
        section.parameters.append(new_param)
        self._rebuild_workspace()

    def _del_layout_item(self):
        # Remove selected item
        tree = None
        if self.left_tree.selectedItems(): tree = self.left_tree
        elif self.right_tree.selectedItems(): tree = self.right_tree
        
        if not tree: return
        
        item = tree.currentItem()
        if not item: return
        
        role = item.data(0, Qt.UserRole)
        obj = item.data(0, Qt.UserRole + 1)
        tab = self._get_current_tab()
        
        if role == "section":
            if obj in tab.parameter_sections:
                 tab.parameter_sections.remove(obj)
        elif role == "parameter":
            section_item = item.parent()
            if section_item:
                section = section_item.data(0, Qt.UserRole + 1)
                if obj in section.parameters:
                    section.parameters.remove(obj)
            
        self._rebuild_workspace()

    def _handle_drop(self, target_tree, target_item, drop_pos):
        """
        MVC Handler for Drag and Drop.
        Manipulates data model then rebuilds UI.
        """
        tab = self._get_current_tab()
        if not tab: return

        # Identify Source
        source_tree = None
        if self.left_tree.selectedItems(): source_tree = self.left_tree
        elif self.right_tree.selectedItems(): source_tree = self.right_tree
        
        if not source_tree: return # Should not happen if dragging
        
        source_item = source_tree.currentItem()
        if not source_item: return
        
        source_role = source_item.data(0, Qt.UserRole)
        source_obj = source_item.data(0, Qt.UserRole + 1)
        
        # Logic for SECTIONS
        if source_role == "section":
            # Target position logic
            target_col = "left" if target_tree == self.left_tree else "right"
            
            # Remove from list
            if source_obj in tab.parameter_sections:
                tab.parameter_sections.remove(source_obj)
            
            # Update position attribute
            source_obj.position = target_col
            
            # Insert at new position
            if target_item:
                target_role = target_item.data(0, Qt.UserRole)
                target_obj = target_item.data(0, Qt.UserRole + 1)
                
                # Verify we are inserting relative to a section in the list
                if target_role == "section":
                    # Find index of target_obj
                    try:
                        idx = tab.parameter_sections.index(target_obj)
                        # Adjust based on drop pos (above/below)
                        if drop_pos == QTreeWidget.BelowItem:
                             idx += 1
                        tab.parameter_sections.insert(idx, source_obj)
                    except ValueError:
                        tab.parameter_sections.append(source_obj) # Fallback
                else:
                     # Dropped on a parameter, put after its section?
                     # Rough logic: append to end of list for now or find section
                     tab.parameter_sections.append(source_obj)
            else:
                # Dropped on whitespace/root
                tab.parameter_sections.append(source_obj)
                
        # Logic for PARAMETERS
        elif source_role == "parameter":
            # Find Source Section
            source_parent_item = source_item.parent()
            if not source_parent_item: return
            source_section = source_parent_item.data(0, Qt.UserRole + 1)
            
            # Identify Target Section
            target_section = None
            insert_idx = -1
            
            if target_item:
                target_role = target_item.data(0, Qt.UserRole)
                target_obj = target_item.data(0, Qt.UserRole + 1)
                
                if target_role == "section":
                    target_section = target_obj
                    insert_idx = 0 if drop_pos == QTreeWidget.AboveItem else len(target_section.parameters)
                elif target_role == "parameter":
                     target_parent = target_item.parent()
                     if target_parent:
                         target_section = target_parent.data(0, Qt.UserRole + 1)
                         try:
                             insert_idx = target_section.parameters.index(target_obj)
                             if drop_pos == QTreeWidget.BelowItem:
                                 insert_idx += 1
                         except ValueError:
                             insert_idx = len(target_section.parameters)
            else:
                # Dropped on root/empty space of a tree
                # Use last section of that tree? Or create new?
                # Probably ignore.
                pass
                
            if target_section:
                # Remove from source
                if source_obj in source_section.parameters:
                    source_section.parameters.remove(source_obj)
                
                # Add to target
                if insert_idx >= 0:
                     target_section.parameters.insert(insert_idx, source_obj)
                else:
                     target_section.parameters.append(source_obj)

        self._rebuild_workspace()

    def _save(self):
        # Reconstruct Data from UI State (Trees specifically) for each tab
        name = self.name_input.text().strip()
        if not name:
            QMessageBox.warning(self, "Error", "Config name cannot be empty.")
            return

        # Prepare Dict for ConfigManager
        config_data = {"tabs": []}
        for tab in self.tabs:
            # We need to serialize our objects back to dicts
            t_dict = asdict(tab)
            # Post-process to map min_value/max_value back to min/max for parameters
            for section in t_dict.get("parameter_sections", []):
                for param in section.get("parameters", []):
                    if "min_value" in param and param["min_value"] is not None:
                        param["min"] = param.pop("min_value")
                    elif "min_value" in param: # Remove None
                         param.pop("min_value")
                         
                    if "max_value" in param and param["max_value"] is not None:
                        param["max"] = param.pop("max_value")
                    elif "max_value" in param: # Remove None
                         param.pop("max_value")

            config_data["tabs"].append(t_dict)
            
        if self.config_manager.save_user_config(name, config_data):
            if self.mode == 'edit' and name != self.original_config_name:
                self.config_manager.delete_user_config(self.original_config_name)
            self.accept()
        else:
             QMessageBox.critical(self, "Error", "Failed to save configuration.")
