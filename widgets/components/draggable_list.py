"""
Draggable List Widget

Custom list widget with drag and drop reordering capabilities,
integrated with the theme manager for dynamic styling.
"""

from PySide6.QtWidgets import QListWidget
from PySide6.QtCore import Qt, Signal
from widgets.mixins import ThemedWidgetMixin
from core.theme_manager import get_theme_manager


class DraggableListWidget(QListWidget, ThemedWidgetMixin):
    """Custom list widget with drag and drop reordering and theme integration"""
    
    order_changed = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        ThemedWidgetMixin.__init__(self)
        
        # Enable drag and drop
        self.setDragDropMode(QListWidget.InternalMove)
        self.setDefaultDropAction(Qt.MoveAction)
        self.setSelectionMode(QListWidget.SingleSelection)
        
        # Apply initial theme
        self._apply_theme()
        
    def _apply_theme(self):
        """Apply theme colors to the list widget"""
        tm = get_theme_manager()
        
        # Get colors from theme
        bg = tm.get_color('draggable_list.background') or tm.get_color('backgrounds.input')
        border = tm.get_color('draggable_list.border') or tm.get_color('borders.inactive')
        item_bg = tm.get_color('draggable_list.item_background') or tm.get_color('backgrounds.tertiary')
        item_border = tm.get_color('draggable_list.item_border') or tm.get_color('borders.inactive')
        item_sel_bg = tm.get_color('draggable_list.item_selected_background') or tm.get_color('accents.primary')
        item_sel_text = tm.get_color('draggable_list.item_selected_text') or tm.get_color('backgrounds.primary')
        item_hover_bg = tm.get_color('draggable_list.item_hover_background') or tm.get_color('borders.inactive')
        item_hover_border = tm.get_color('draggable_list.item_hover_border') or tm.get_color('borders.active')
        text_color = tm.get_color('text.primary')
        
        # Get style values
        border_radius = tm.get_style('draggable_list.border_radius') or 4
        item_border_radius = tm.get_style('draggable_list.item_border_radius') or 3
        item_padding = tm.get_style('draggable_list.item_padding') or 6
        item_margin = tm.get_style('draggable_list.item_margin') or 2
        
        # Apply stylesheet
        self.setStyleSheet(f"""
            QListWidget {{
                background-color: {bg};
                color: {text_color};
                border: 1px solid {border};
                border-radius: {border_radius}px;
                padding: 4px;
                outline: none;
            }}
            QListWidget::item {{
                background-color: {item_bg};
                border: 1px solid {item_border};
                border-radius: {item_border_radius}px;
                padding: {item_padding}px;
                margin: {item_margin}px;
            }}
            QListWidget::item:selected {{
                background-color: {item_sel_bg};
                color: {item_sel_text};
                border: 1px solid {item_sel_bg};
            }}
            QListWidget::item:hover {{
                background-color: {item_hover_bg};
                border: 1px solid {item_hover_border};
            }}
        """)
    
    def dropEvent(self, event):
        """Handle drop event and emit signal"""
        super().dropEvent(event)
        self.order_changed.emit()
