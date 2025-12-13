"""
Order Widget

Resizable widget for configuring lock and hinge execution order,
integrated with the theme manager for dynamic styling.
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QListWidgetItem, QLabel
from PySide6.QtCore import Qt, Signal
from widgets.mixins import ThemedWidgetMixin
from widgets.primitives.buttons import PurpleButton
from widgets.components.draggable_list import DraggableListWidget
from core.theme_manager import get_theme_manager


class OrderWidget(QWidget, ThemedWidgetMixin):
    """Resizable widget for configuring lock and hinge execution order"""
    
    order_changed = Signal(list)  # Emits list of items in order
    
    def __init__(self, parent=None):
        super().__init__(parent)
        ThemedWidgetMixin.__init__(self)
        self.setup_ui()
        
    def setup_ui(self):
        """Setup UI components"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        tm = get_theme_manager()
        
        # Title
        title = QLabel("Execution Order")
        title_color = tm.get_color('text.primary') or '#ffffff'
        title.setStyleSheet(f"QLabel {{ font-weight: bold; padding: 5px; color: {title_color}; }}")
        layout.addWidget(title)
        
        # Instructions
        instructions = QLabel("Drag items to reorder execution sequence:")
        inst_color = tm.get_color('text.secondary') or '#bdbdc0'
        instructions.setStyleSheet(f"QLabel {{ color: {inst_color}; font-size: 11px; }}")
        layout.addWidget(instructions)
        
        # Draggable list - now resizable by user
        self.order_list = DraggableListWidget()
        self.order_list.setMinimumHeight(100)  # Minimum height
        self.order_list.order_changed.connect(self.emit_order_changed)
        layout.addWidget(self.order_list, 1)  # Give it stretch factor
        
        # Control buttons
        button_layout = QHBoxLayout()
        layout.addLayout(button_layout)
        
        self.move_up_btn = PurpleButton("↑ Up")
        self.move_up_btn.clicked.connect(self.move_up)
        button_layout.addWidget(self.move_up_btn)
        
        self.move_down_btn = PurpleButton("↓ Down")
        self.move_down_btn.clicked.connect(self.move_down)
        button_layout.addWidget(self.move_down_btn)
        
        button_layout.addStretch()
    
    def _apply_theme(self):
        """Apply theme - labels are updated in setup_ui when theme changes"""
        # Labels need to be recreated or their stylesheets updated
        # For now, widgets will update on next instantiation
        pass
    
    def update_items(self, lock_active, hinge_count, hinge_active):
        """Update the list based on active components"""
        self.order_list.clear()
        
        # Add lock if active
        if lock_active:
            item = QListWidgetItem("Lock")
            item.setData(Qt.UserRole, "lock")
            self.order_list.addItem(item)
        
        # Add active hinges
        for i in range(hinge_count):
            if i < len(hinge_active) and hinge_active[i]:
                item = QListWidgetItem(f"Hinge {i+1}")
                item.setData(Qt.UserRole, f"hinge{i+1}")
                self.order_list.addItem(item)
        
        self.emit_order_changed()
    
    def move_up(self):
        """Move selected item up"""
        current_row = self.order_list.currentRow()
        if current_row > 0:
            item = self.order_list.takeItem(current_row)
            self.order_list.insertItem(current_row - 1, item)
            self.order_list.setCurrentRow(current_row - 1)
            self.emit_order_changed()
    
    def move_down(self):
        """Move selected item down"""
        current_row = self.order_list.currentRow()
        if current_row < self.order_list.count() - 1:
            item = self.order_list.takeItem(current_row)
            self.order_list.insertItem(current_row + 1, item)
            self.order_list.setCurrentRow(current_row + 1)
            self.emit_order_changed()
    
    def emit_order_changed(self):
        """Emit the current order"""
        order = []
        for i in range(self.order_list.count()):
            item = self.order_list.item(i)
            order.append(item.data(Qt.UserRole))
        self.order_changed.emit(order)
    
    def get_order(self):
        """Get current execution order"""
        order = []
        for i in range(self.order_list.count()):
            item = self.order_list.item(i)
            order.append(item.data(Qt.UserRole))
        return order
    
    def set_order(self, order_list):
        """Set the execution order"""
        self.order_list.clear()
        
        for item_id in order_list:
            if item_id == "lock":
                item = QListWidgetItem("Lock")
                item.setData(Qt.UserRole, "lock")
                self.order_list.addItem(item)
            elif item_id.startswith("hinge"):
                hinge_num = item_id.replace("hinge", "")
                item = QListWidgetItem(f"Hinge {hinge_num}")
                item.setData(Qt.UserRole, item_id)
                self.order_list.addItem(item)
