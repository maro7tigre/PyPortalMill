from PySide6.QtWidgets import QFrame, QVBoxLayout
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QPixmap

from ..primitives.labels import ThemedLabel, ClickableImageLabel
from widgets.mixins import ThemedWidgetMixin
from .menus import ThemedMenu
from ..utils import PlaceholderPixmap
from core.theme_manager import get_theme_manager

class SelectableItem(QFrame, ThemedWidgetMixin):
    """Base class for selectable items with interactions"""
    clicked = Signal(str)
    edit_requested = Signal(str)
    duplicate_requested = Signal(str)
    delete_requested = Signal(str)
    
    def __init__(self, name, is_add_button=False, parent=None):
        super().__init__(parent)
        ThemedWidgetMixin.__init__(self)
        self.name = name
        self.is_add_button = is_add_button
        self.selected = False
        self._is_hovered = False
        self.setCursor(Qt.PointingHandCursor)
        
    def set_selected(self, selected):
        self.selected = selected
        self.update_style()
    
    def enterEvent(self, event):
        if not self.selected:
            self._is_hovered = True
            self.update_style()
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        self._is_hovered = False
        self.update_style()
        super().leaveEvent(event)
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit(self.name)
        elif event.button() == Qt.RightButton and not self.is_add_button:
            self.show_context_menu(event.globalPos())
            
    def show_context_menu(self, pos):
        menu = ThemedMenu(self)
        edit_action = menu.addAction("Edit")
        duplicate_action = menu.addAction("Duplicate")
        menu.addSeparator()
        delete_action = menu.addAction("Delete")
        
        action = menu.exec_(pos)
        if action == edit_action:
            self.edit_requested.emit(self.name)
        elif action == duplicate_action:
            self.duplicate_requested.emit(self.name)
        elif action == delete_action:
            self.delete_requested.emit(self.name)
            
    def on_theme_changed(self, theme_name):
        self.update_style()
        
    def update_style(self):
        # Override in subclasses or implement generic style here
        pass

class CardItem(SelectableItem):
    """Generic card item with image and text"""
    def __init__(self, name, size=(120, 140), image_size=(100, 100), 
                 image_data=None, is_add_button=False, parent=None):
        super().__init__(name, is_add_button, parent)
        self.setFixedSize(*size)
        self.image_size = image_size
        self.image_data = image_data
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        
        # Image 
        self.image_label = ClickableImageLabel(image_size)
        self.image_label.setScaledContents(True)
        # Disconnect internal click to avoid double signals, we handle it in SelectableItem
        # self.image_label.clicked.connect(...) 
        self.update_image()
        layout.addWidget(self.image_label, alignment=Qt.AlignCenter)
        
        # Name
        self.name_label = ThemedLabel(name)
        self.name_label.setAlignment(Qt.AlignCenter)
        self.name_label.setWordWrap(True)
        layout.addWidget(self.name_label)
        
        self.update_style()
        
    def update_image(self):
        if self.is_add_button:
            pixmap = PlaceholderPixmap.create_add_button(self.image_size)
        elif self.image_data:
            if isinstance(self.image_data, str):
                pixmap = QPixmap(self.image_data)
            else:
                pixmap = self.image_data
            if pixmap and not pixmap.isNull():
                pixmap = pixmap.scaled(*self.image_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            else:
                pixmap = PlaceholderPixmap.create_file_icon(self.image_size)
        else:
            pixmap = PlaceholderPixmap.create_file_icon(self.image_size)
        self.image_label.setPixmap(pixmap)

    def update_style(self):
        tm = get_theme_manager()
        
        if self.selected:
            bg = "#1A2E20" # TODO: Get from theme (e.g., success.dark)
            border = tm.get_color("accents.secondary") # Green
            width = 3
        elif self._is_hovered:
            bg = "#3a3d4d" # TODO: theme.hover
            border = tm.get_color("borders.active") # Purple
            width = 2
        else:
            bg = tm.get_color("backgrounds.tertiary")
            border = tm.get_color("borders.inactive")
            width = 2
            
        self.setStyleSheet(f"""
            {self.__class__.__name__} {{
                background-color: {bg};
                border: {width}px solid {border};
                border-radius: 4px;
            }}
        """)
        self.update()

class ProfileItem(CardItem):
    """Individual profile item widget"""
    def __init__(self, name, profile_data=None, is_add_button=False, parent=None):
        image_data = profile_data.get("image") if profile_data else None
        super().__init__(name, size=(120, 140), image_size=(100, 100), 
                       image_data=image_data, is_add_button=is_add_button, parent=parent)

class TypeItem(CardItem):
    """Individual type item widget"""
    def __init__(self, name, image_path=None, is_add_button=False, parent=None):
        super().__init__(name, size=(100, 120), image_size=(80, 80), 
                       image_data=image_path, is_add_button=is_add_button, parent=parent)
        
    def update_image(self):
        if not self.image_data and not self.is_add_button:
             pixmap = PlaceholderPixmap.create_type_placeholder(self.image_size)
             self.image_label.setPixmap(pixmap)
        else:
            super().update_image()

class StatusCard(QFrame, ThemedWidgetMixin):
    """Card displaying a status state"""
    clicked = Signal()
    STATE_NEUTRAL = "neutral"
    STATE_VALID = "valid"
    STATE_CHANGED = "changed"
    
    def __init__(self, title, description="", state=STATE_NEUTRAL, parent=None):
        super().__init__(parent)
        ThemedWidgetMixin.__init__(self)
        self.title = title
        self.state = state
        
        self.setFixedSize(160, 100)
        self.setCursor(Qt.PointingHandCursor)
        
        layout = QVBoxLayout(self)
        self.lbl_title = ThemedLabel(title)
        self.lbl_title.setStyleSheet("font-weight: bold; font-size: 14px; border: none; background: transparent;")
        layout.addWidget(self.lbl_title)
        
        if description:
            self.lbl_desc = ThemedLabel(description)
            self.lbl_desc.setStyleSheet("color: #8b95c0; font-size: 11px; border: none; background: transparent;")
            self.lbl_desc.setWordWrap(True)
            layout.addWidget(self.lbl_desc)
            
        layout.addStretch()
        
        self.bar = QFrame()
        self.bar.setFixedHeight(4)
        layout.addWidget(self.bar)
        
        self.update_style()
        
    def set_state(self, state):
        self.state = state
        self.update_style()
        
    def on_theme_changed(self, theme_name):
        self.update_style()
        
    def update_style(self):
        tm = get_theme_manager()
        
        if self.state == self.STATE_VALID:
            bg = tm.get_color("status_card.valid") or "#1A2E20" 
            border = tm.get_color("accents.secondary") 
            bar_color = tm.get_color("accents.secondary")
        elif self.state == self.STATE_CHANGED:
            bg = tm.get_color("status_card.changed") or "#3E2723"
            border = tm.get_color("accents.warning") 
            bar_color = tm.get_color("accents.warning")
        else:
            bg = tm.get_color("status_card.neutral") or tm.get_color("backgrounds.tertiary")
            border = tm.get_color("borders.inactive")
            bar_color = tm.get_color("text.disabled")
            
        self.setStyleSheet(f"""
            StatusCard {{
                background-color: {bg};
                border: 2px solid {border};
                border-radius: 6px;
            }}
        """)
        self.bar.setStyleSheet(f"background-color: {bar_color}; border-radius: 2px;")
        
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()
