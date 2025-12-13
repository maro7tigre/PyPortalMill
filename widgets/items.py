"""
Item Widgets Module

Contains individual item widgets with selection, hover, and context menu support.
Now refactored with a shared CardItem base class.
"""

from PySide6.QtWidgets import QFrame, QVBoxLayout, QWidget
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QPixmap, QColor, QPainter

from .primitives.labels import ThemedLabel, ClickableImageLabel
from .primitives.containers import ThemedMenu
from .utils import PlaceholderPixmap


class SelectableItem(QFrame):
    """Base class for selectable items with interactions"""
    
    clicked = Signal(str)
    edit_requested = Signal(str)
    duplicate_requested = Signal(str)
    delete_requested = Signal(str)
    
    def __init__(self, name, is_add_button=False, parent=None):
        super().__init__(parent)
        self.name = name
        self.is_add_button = is_add_button
        self.selected = False
        self._is_hovered = False
        
        self.setCursor(Qt.PointingHandCursor)
        
    def set_selected(self, selected):
        self.selected = selected
        self.update_style()
    
    def update_style(self):
        pass
    
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


class CardItem(SelectableItem):
    """Generic card item with image and text"""
    
    def __init__(self, name, size=(120, 140), image_size=(100, 100), 
                 image_data=None, is_add_button=False, parent=None):
        super().__init__(name, is_add_button, parent)
        self.setFixedSize(*size)
        self.image_size = image_size
        self.image_data = image_data
        
        # Layout
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
        """Update displayed image - can be overridden or used as is"""
        if self.is_add_button:
            pixmap = PlaceholderPixmap.create_add_button(self.image_size)
        elif self.image_data:
            # Handle string path
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
        """Apply styling based on current state"""
        from core.theme_manager import get_theme_manager
        tm = get_theme_manager()
        theme = tm.current_theme
        
        # Default fallback values
        styles = {
            "neutral": {"background": "#44475c", "border": "#6f779a"},
            "hovered": {"background": "#3a3d4d", "border": "#8b95c0"},
            "selected": {"background": "#1A2E20", "border": "#23c87b"}
        }
        
        # Override with theme values if available
        if theme and 'cards' in theme:
            cards = theme['cards']
            if 'neutral' in cards: styles['neutral'] = cards['neutral']
            if 'hovered' in cards: styles['hovered'] = cards['hovered']
            if 'selected' in cards: styles['selected'] = cards['selected']
            
            # Use geometric styles from control_styles if available
            c_styles = theme.get('control_styles', {}).get('cards', {})
            radius = c_styles.get('border_radius', 4)
            border_w = c_styles.get('border_width', 2)
        else:
            radius = 4
            border_w = 2

        if self.selected:
            s = styles['selected']
        elif self._is_hovered:
            s = styles['hovered']
        else:
            s = styles['neutral']
            
        self.setStyleSheet(f"""
            {self.__class__.__name__} {{
                background-color: {s.get('background')};
                border: {border_w}px solid {s.get('border')};
                border-radius: {radius}px;
            }}
        """)
        
        # Apply Dimensions if present in theme
        c_styles = theme.get('control_styles', {}).get('cards', {})
        width = c_styles.get('width', 120)
        height = c_styles.get('height', 140)
        img_size = c_styles.get('image_size', 100)
        font_size = c_styles.get('font_size', 12)
        
        self.setFixedSize(width, height)
        if hasattr(self, 'image_label'):
             self.image_label.setFixedSize(img_size, img_size)
             self.image_size = (img_size, img_size)
             # Trigger image update to rescale if needed
             self.update_image()
             
        if hasattr(self, 'name_label'):
            f = self.name_label.font()
            f.setPointSize(font_size)
            self.name_label.setFont(f)

        self.update()


class ProfileItem(CardItem):
    """Individual profile item widget"""
    
    def __init__(self, name, profile_data=None, is_add_button=False, parent=None):
        # Extract image from profile_data
        image_data = profile_data.get("image") if profile_data else None
        super().__init__(name, size=(120, 140), image_size=(100, 100), 
                       image_data=image_data, is_add_button=is_add_button, parent=parent)


class TypeItem(CardItem):
    """Individual type item widget"""
    
    def __init__(self, name, image_path=None, is_add_button=False, parent=None):
        super().__init__(name, size=(100, 120), image_size=(80, 80), 
                       image_data=image_path, is_add_button=is_add_button, parent=parent)
        
    def update_image(self):
        # Allow default behavior but fallback to type specific placeholder 
        if not self.image_data and not self.is_add_button:
             pixmap = PlaceholderPixmap.create_type_placeholder(self.image_size)
             self.image_label.setPixmap(pixmap)
        else:
            super().update_image()


class StatusCard(QFrame):
    """Card displaying a status state (Neutral, Valid, Changed)"""
    
    clicked = Signal()
    
    # States
    STATE_NEUTRAL = "neutral"
    STATE_VALID = "valid"
    STATE_CHANGED = "changed"
    
    def __init__(self, title, description="", state=STATE_NEUTRAL, parent=None):
        super().__init__(parent)
        self.title = title
        self.state = state
        
        self.setFixedSize(160, 100)
        self.setCursor(Qt.PointingHandCursor)
        
        layout = QVBoxLayout(self)
        
        # Title
        self.lbl_title = ThemedLabel(title)
        self.lbl_title.setStyleSheet("font-weight: bold; font-size: 14px; border: none; background: transparent;")
        layout.addWidget(self.lbl_title)
        
        # Description
        if description:
            self.lbl_desc = ThemedLabel(description)
            self.lbl_desc.setStyleSheet("color: #8b95c0; font-size: 11px; border: none; background: transparent;")
            self.lbl_desc.setWordWrap(True)
            layout.addWidget(self.lbl_desc)
            
        layout.addStretch()
        
        # Status Icon/Indicator (simple colored bar at bottom)
        self.bar = QFrame()
        self.bar.setFixedHeight(4)
        layout.addWidget(self.bar)
        
        self.update_style()
        
    def set_state(self, state):
        self.state = state
        self.update_style()
        
    def update_style(self):
        from core.theme_manager import get_theme_manager
        tm = get_theme_manager()
        
        # Default Hardcoded Fallbacks
        colors = {
            "valid": {"bg": "#1A2E20", "border": "#23c87b", "bar": "#23c87b"},
            "changed": {"bg": "#3E2723", "border": "#FF9800", "bar": "#FF9800"},
            "neutral": {"bg": "#44475c", "border": "#6f779a", "bar": "#8b95c0"}
        }
        
        # Override from theme if available
        # The editor uses 'status_card.valid' (single color?) or object?
        # StatusSection.py uses: add_color_control("Valid State", "status_card.valid", ...)
        # It seems it only sets one color for the Valid state? likely the border/bar or background?
        # Let's assume the user meant the main accent color, but for full control we might need more.
        # However, to be safe and compatible with existing StatusSection, let's see what it sets.
        # It sets "status_card.valid" to a specific color hex string.
        
        # Let's use that color for border/bar, and maybe a dark version for BG?
        # Or check if 'status_card' is a dict with subkeys.
        
        theme = tm.current_theme
        sc = theme.get('status_card', {}) if theme else {}
        
        if isinstance(sc, dict): 
            # If we updated StatusSection to be more detailed, we could use dict.
            # But currently StatusSection sets string values for 'valid', 'changed', 'neutral'.
            pass
            
        # For now, let's try to fetch specific keys if they exist, or fallback to the single color for border/bar
        
        def get_state_colors(state_key, default_set):
            # Check if there's a simple color defined
            primary = tm.get_color(f"status_card.{state_key}")
            
            if primary and primary != "#000000":
                # Use this primary color for border & bar
                # Use a derived or hardcoded dark for BG? Or maybe bg_tertiary?
                return {"bg": default_set["bg"], "border": primary, "bar": primary}
            return default_set

        s_colors = get_state_colors(self.state, colors.get(self.state, colors["neutral"]))

        bg_color = s_colors["bg"]
        border_color = s_colors["border"]
        bar_color = s_colors["bar"]
        
        self.setStyleSheet(f"""
            StatusCard {{
                background-color: {bg_color};
                border: 2px solid {border_color};
                border-radius: 6px;
            }}
        """)
        self.bar.setStyleSheet(f"background-color: {bar_color}; border-radius: 2px;")
        
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()
