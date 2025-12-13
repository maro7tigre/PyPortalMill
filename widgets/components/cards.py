from PySide6.QtWidgets import QFrame, QVBoxLayout
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QPixmap

from ..primitives.labels import ThemedLabel, ClickableImageLabel
from widgets.mixins import ThemedWidgetMixin
from widgets.primitives.containers import ThemedMenu
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
                 image_data=None, is_add_button=False, parent=None, style_prefix="cards.generic"):
        super().__init__(name, is_add_button, parent)
        self.style_prefix = style_prefix
        self.default_size = size
        self.default_image_size = image_size
        
        # Initial sizing (will be updated by theme)
        self.setFixedSize(*size)
        self.image_size = image_size
        self.image_data = image_data
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        
        # Image 
        self.image_label = ClickableImageLabel(image_size)
        self.image_label.setScaledContents(True)
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
        
        # 1. Update Dimensions from Theme (control_styles)
        def get_dim(prop, default):
            val = tm.get_style(f"{self.style_prefix}.{prop}")
            if val is None:
                val = tm.get_style(f"cards.{prop}")
            return int(val) if val is not None else default

        w = get_dim("width", self.default_size[0])
        h = get_dim("height", self.default_size[1])
        img_w = get_dim("image_size_w", self.default_image_size[0])
        img_h = get_dim("image_size_h", self.default_image_size[1])
        f_size = get_dim("font_size", 12)
        
        if self.width() != w or self.height() != h:
            self.setFixedSize(w, h)
            
        if self.image_size != (img_w, img_h):
            self.image_size = (img_w, img_h)
            self.image_label.setFixedSize(img_w, img_h)
            self.update_image()
            
        # 2. Update Colors & Borders
        prefix = self.style_prefix 
        
        if self.selected:
            state = "selected"
            default_bg = "#1A2E20"
            default_border = "#23c87b"
        elif self._is_hovered:
            state = "hovered"
            default_bg = "#3a3d4d"
            default_border = "#8b95c0"
        else:
            state = "neutral"
            default_bg = "#44475c"
            default_border = "#6f779a"
            
        def get_color_safe(key, default):
            path = f"{prefix}.{state}.{key}"
            # Manual lookup to distinguish missing vs black
            parts = path.split('.')
            curr = tm.current_theme
            for p in parts:
                if isinstance(curr, dict) and p in curr:
                    curr = curr[p]
                else:
                    return default
            return curr
        
        bg = get_color_safe("background", default_bg)
        border_color = get_color_safe("border", default_border)
        text_color = get_color_safe("text", "#ffffff")
        
        b_radius = tm.get_style(f"{prefix}.{state}.border_radius")
        if b_radius is None: 
            b_radius = tm.get_style(f"{prefix}.border_radius")
        if b_radius is None: b_radius = 4
        
        b_width = tm.get_style(f"{prefix}.{state}.border_width")
        if b_width is None: 
            b_width = tm.get_style(f"{prefix}.border_width")
        if b_width is None: b_width = 2
            
        self.setStyleSheet(f"""
            {self.__class__.__name__} {{
                background-color: {bg};
                border: {b_width}px solid {border_color};
                border-radius: {b_radius}px;
            }}
        """)
        
        self.name_label.setStyleSheet(f"color: {text_color}; font-size: {f_size}pt; border: none; background: transparent;")
        self.update()

class ProfileItem(CardItem):
    """Individual profile item widget"""
    def __init__(self, name, profile_data=None, is_add_button=False, parent=None):
        image_data = profile_data.get("image") if profile_data else None
        super().__init__(name, size=(120, 140), image_size=(100, 100), 
                       image_data=image_data, is_add_button=is_add_button, parent=parent,
                       style_prefix="cards.profile")

class TypeItem(CardItem):
    """Individual type item widget"""
    def __init__(self, name, image_path=None, is_add_button=False, parent=None):
        super().__init__(name, size=(100, 120), image_size=(80, 80), 
                       image_data=image_path, is_add_button=is_add_button, parent=parent,
                       style_prefix="cards.type")
        
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
        from core.theme_manager import get_theme_manager
        tm = get_theme_manager()
        theme = tm.current_theme
        
        # Helper to get deep value safely or return default
        def get_val(state, key, default):
            # Try specific path: status_card.<state>.<key>
            val = tm.get_style(f"status_card.{state}.{key}")
            
            sc = theme.get('status_card', {})
            if isinstance(sc, dict):
                 st = sc.get(state, {})
                 if isinstance(st, dict):
                     return st.get(key, default)
                 # Fallback if state is just a string (old format) -> use it as border/bar color
                 if key in ["border", "bar"]:
                     # If previous value was string, it was a color hex
                     if isinstance(st, str): return st
            return default

        # Defaults
        defaults = {
            "neutral": {
                "background": "#44475c", "border": "#8b95c0", "title_size": 14, 
                "title_color": "#ffffff", "msg_size": 11, "msg_color": "#8b95c0"
            },
            "valid": {
                "background": "#1A2E20", "border": "#23c87b", "title_size": 14, 
                "title_color": "#ffffff", "msg_size": 11, "msg_color": "#23c87b"
            },
            "changed": {
                "background": "#3E2723", "border": "#FF9800", "title_size": 14, 
                "title_color": "#ffffff", "msg_size": 11, "msg_color": "#FF9800"
            }
        }
        
        d = defaults.get(self.state, defaults["neutral"])
        
        bg = get_val(self.state, "background", d["background"])
        border = get_val(self.state, "border", d["border"])
        t_size = get_val(self.state, "title_size", d["title_size"])
        t_color = get_val(self.state, "title_color", d["title_color"])
        m_size = get_val(self.state, "msg_size", d["msg_size"])
        m_color = get_val(self.state, "msg_color", d["msg_color"])
        
        # Normalize types
        try: t_size = int(t_size)
        except: t_size = 14
        try: m_size = int(m_size)
        except: m_size = 11
        
        self.setStyleSheet(f"""
            StatusCard {{
                background-color: {bg};
                border: 2px solid {border};
                border-radius: 6px;
            }}
        """)
        self.bar.setStyleSheet(f"background-color: {border}; border-radius: 2px;")
        
        # Update Labels
        self.lbl_title.setStyleSheet(f"font-weight: bold; font-size: {t_size}px; color: {t_color}; border: none; background: transparent;")
        
        if hasattr(self, 'lbl_desc'):
            self.lbl_desc.setStyleSheet(f"font-size: {m_size}px; color: {m_color}; border: none; background: transparent;")
        
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()
