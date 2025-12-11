from PySide6.QtWidgets import (QTreeWidget, QTreeWidgetItem, QWidget, QFormLayout, 
                               QLineEdit, QSpinBox, QDoubleSpinBox, QCheckBox, 
                               QComboBox, QLabel, QVBoxLayout, QGroupBox, QPushButton, QColorDialog)
from PySide6.QtCore import Qt, Signal, QMimeData
from PySide6.QtGui import QDrag, QAction, QColor

class DraggableTreeWidget(QTreeWidget):
    """
    Tree widget supporting drag and drop of Sections and Parameters.
    Emits a signal for the controller to handle the data update.
    """
    # Emits (target_item, drop_indicator_position)
    drop_requested = Signal(object, object) 

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDragDropMode(QTreeWidget.DragDrop)
        self.setDefaultDropAction(Qt.MoveAction)
        self.setSelectionMode(QTreeWidget.SingleSelection)
        self.setHeaderHidden(True)
        
    def mimeTypes(self):
        return ['application/x-qabstractitemmodeldatalist']

    def dropEvent(self, event):
        # We override dropEvent to INTERCEPT the drop.
        # We do NOT call super().dropEvent(event) because we don't want the visual move 
        # to happen automatically. We want the Controller to update the Data and Rebuild.
        
        target = self.itemAt(event.position().toPoint())
        drop_pos = self.dropIndicatorPosition()
        
        # Accept the event so the drag operation concludes
        event.accept()
        
        # Emit signal for the dialog to handle data changes
        self.drop_requested.emit(target, drop_pos)

class PropertiesEditor(QWidget):
    """
    Dynamic form to edit properties of the selected object.
    """
    data_changed = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.current_obj = None
        self.form_layout = None
        
    def edit_object(self, obj, obj_type):
        """Build form for the object"""
        self.current_obj = obj
        
        # Clear previous
        if self.form_layout:
             # Remove all widgets
             while self.form_layout.count():
                 item = self.form_layout.takeAt(0)
                 widget = item.widget()
                 if widget:
                     widget.deleteLater()
             self.layout.removeItem(self.form_layout)
             
        self.form_layout = QFormLayout()
        self.layout.addLayout(self.form_layout)
        
        if obj_type == "tab":
            self._build_tab_form(obj)
        elif obj_type == "profile":
            self._build_profile_form(obj)
        elif obj_type == "section":
            self._build_section_form(obj)
        elif obj_type == "parameter":
            self._build_parameter_form(obj)
        elif obj_type == "preview_shape":
            self._build_preview_shape_form(obj)
            
    def _build_preview_shape_form(self, shape):
        self._add_text_input("ID", shape, "id")
        self._add_text_input("Type", shape, "type", read_only=True)
        # Position/Size can be string (equation) or float
        self._add_text_input("X", shape, "x")
        self._add_text_input("Y", shape, "y")
        self._add_text_input("Width", shape, "width")
        self._add_text_input("Height", shape, "height")
        self._add_color_input("Color", shape, "color")
        self._add_color_input("Border Color", shape, "border_color")
        self._add_number_input("Border Width", shape, "border_width", "int")
            
    def _build_tab_form(self, tab):
        self._add_text_input("ID", tab, "id", read_only=True) # ID usually fixed or specific logic
        self._add_text_input("Name", tab, "name")
        self._add_combo("Profile Validation", tab, "profile_validation", ["none", "require_one", "require_all"])

    def _build_profile_form(self, profile):
        self._add_text_input("ID", profile, "id")
        self._add_text_input("Name", profile, "name")
        self._add_text_input("Type", profile, "type")
        self._add_checkbox("Required", profile, "is_required")
        # Shared With list editing - simplified as comma separated string for now
        self._add_list_input("Shared With", profile, "shared_with")

    def _build_section_form(self, section):
        self._add_text_input("ID", section, "id")
        self._add_text_input("Title", section, "title")
        # Position is now determined by the UI column (Left/Right Tree), so we remove the edit field.
        # self._add_combo("Position", section, "position", ["left", "right"])

    def _build_parameter_form(self, param):
        self._add_text_input("Name", param, "name")
        self._add_text_input("Label", param, "label")
        self._add_combo("Type", param, "type", ["string", "int", "float", "bool", "enum"])
        
        # Default value handling based on type
        if param.type == "bool":
            self._add_checkbox("Default", param, "default")
        elif param.type in ["int", "float"]:
             self._add_number_input("Default", param, "default", param.type)
             self._add_number_input("Min", param, "min_value", param.type)
             self._add_number_input("Max", param, "max_value", param.type)
        else:
            self._add_text_input("Default", param, "default")
            
        if param.type == "enum":
             self._add_list_input("Options", param, "options")
             
        self._add_checkbox("Has Auto", param, "has_auto")

    def _add_text_input(self, label, obj, attr, read_only=False):
        val = getattr(obj, attr, "")
        widget = QLineEdit(str(val))
        widget.setReadOnly(read_only)
        if not read_only:
             widget.textChanged.connect(lambda text: self._update_attr(obj, attr, text))
        self.form_layout.addRow(label, widget)
        
    def _add_number_input(self, label, obj, attr, type_str):
        val = getattr(obj, attr)
        if val is None: val = 0
        
        if type_str == "int":
            widget = QSpinBox()
            widget.setRange(-9999, 9999)
            widget.setValue(int(val))
            widget.valueChanged.connect(lambda v: self._update_attr(obj, attr, v))
        else:
            widget = QDoubleSpinBox()
            widget.setRange(-9999.0, 9999.0)
            widget.setValue(float(val))
            widget.valueChanged.connect(lambda v: self._update_attr(obj, attr, v))
            
        self.form_layout.addRow(label, widget)

    def _add_checkbox(self, label, obj, attr):
        val = getattr(obj, attr, False)
        widget = QCheckBox()
        widget.setChecked(bool(val))
        widget.toggled.connect(lambda v: self._update_attr(obj, attr, v))
        self.form_layout.addRow(label, widget)

    def _add_combo(self, label, obj, attr, options):
        val = getattr(obj, attr, options[0] if options else "")
        widget = QComboBox()
        widget.addItems(options)
        widget.setCurrentText(str(val))
        widget.currentTextChanged.connect(lambda text: self._update_attr(obj, attr, text))
         # Rebuild form if type changes (for parameters)
        if attr == "type":
             widget.currentTextChanged.connect(lambda: self.edit_object(obj, "parameter"))
             
        self.form_layout.addRow(label, widget)
        
    def _add_list_input(self, label, obj, attr):
        val = getattr(obj, attr, [])
        text_val = ", ".join(val) if val else ""
        widget = QLineEdit(text_val)
        widget.setPlaceholderText("Comma separated values")
        widget.textChanged.connect(lambda text: self._update_attr(obj, attr, [x.strip() for x in text.split(",") if x.strip()]))
        self.form_layout.addRow(label, widget)

        self.form_layout.addRow(label, widget)

    def _add_color_input(self, label, obj, attr):
        val = getattr(obj, attr, "#000000")
        
        btn = QPushButton()
        btn.setFixedSize(60, 24)
        btn.setStyleSheet(f"background-color: {val}; border: 1px solid #666;")
        
        def pick_color():
            current = QColor(getattr(obj, attr, "#000000"))
            color = QColorDialog.getColor(current, self, f"Select {label}")
            if color.isValid():
                hex_color = color.name()
                btn.setStyleSheet(f"background-color: {hex_color}; border: 1px solid #666;")
                self._update_attr(obj, attr, hex_color)
                
        btn.clicked.connect(pick_color)
        self.form_layout.addRow(label, btn)

    def _update_attr(self, obj, attr, value):
        setattr(obj, attr, value)
        self.data_changed.emit()
