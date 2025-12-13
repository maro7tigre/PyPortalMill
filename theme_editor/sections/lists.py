"""
Draggable Lists Section for Theme Editor
"""

from PySide6.QtWidgets import QLabel, QVBoxLayout, QListWidgetItem
from PySide6.QtCore import Qt
from ..base_section import ThemeEditorSection
from widgets.components.draggable_list import DraggableListWidget
from widgets.components.order_widget import OrderWidget


class ListsSection(ThemeEditorSection):
    def setup_config_ui(self):
        """Setup configuration controls"""
        self.add_header("List Container")
        self.add_color_control("Background", "draggable_list.background", "#1d1f28")
        self.add_color_control("Border", "draggable_list.border", "#6f779a")
        self.add_number_control("Border Radius (px)", "styles.draggable_list.border_radius", 4, 0, 20)
        
        self.add_header("List Items")
        self.add_color_control("Item Background", "draggable_list.item_background", "#44475c")
        self.add_color_control("Item Border", "draggable_list.item_border", "#6f779a")
        self.add_number_control("Item Border Radius (px)", "styles.draggable_list.item_border_radius", 3, 0, 10)
        self.add_number_control("Item Padding (px)", "styles.draggable_list.item_padding", 6, 0, 20)
        self.add_number_control("Item Margin (px)", "styles.draggable_list.item_margin", 2, 0, 10)
        
        self.add_header("Item States - Selected")
        self.add_color_control("Selected Background", "draggable_list.item_selected_background", "#BB86FC")
        self.add_color_control("Selected Text", "draggable_list.item_selected_text", "#1d1f28")
        
        self.add_header("Item States - Hover")
        self.add_color_control("Hover Background", "draggable_list.item_hover_background", "#6f779a")
        self.add_color_control("Hover Border", "draggable_list.item_hover_border", "#8b95c0")
        
        self.config_layout.addStretch()
    
    def setup_preview_ui(self):
        """Setup preview widgets"""
        layout = self.preview_inner_layout
        
        # DraggableListWidget preview
        label1 = QLabel("Draggable List") 
        label1.setStyleSheet("font-size: 12px; font-weight: bold; color: #888; margin-bottom: 5px;")
        layout.addWidget(label1)
        
        self.list_preview = DraggableListWidget()
        self.list_preview.setMaximumHeight(150)
        
        # Add sample items
        for i in range(1, 5):
            item = QListWidgetItem(f"Item {i}")
            self.list_preview.addItem(item)
        
        layout.addWidget(self.list_preview)
        
        # OrderWidget preview
        label2 = QLabel("Order Widget (with controls)")
        label2.setStyleSheet("font-size: 12px; font-weight: bold; color: #888; margin-top: 15px; margin-bottom: 5px;")
        layout.addWidget(label2)
        
        self.order_preview = OrderWidget()
        self.order_preview.setMaximumHeight(250)
        
        # Add sample order items
        self.order_preview.update_items(
            lock_active=True,
            hinge_count=3,
            hinge_active=[True, True, True]
        )
        
        layout.addWidget(self.order_preview)
        layout.addStretch()
    
    def update_preview(self):
        """Update preview when theme changes"""
        if hasattr(self, 'list_preview'):
            self.list_preview._apply_theme()
        if hasattr(self, 'order_preview'):
            self.order_preview.order_list._apply_theme()
