"""
Profile Item Widget

Individual profile card widget for displaying profiles in a grid.
Adapted from old version with themed styling.
"""

from PySide6.QtWidgets import QFrame, QVBoxLayout
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QPixmap

from .themed_widgets import ThemedLabel, ThemedMenu
from .simple_widgets import PlaceholderPixmap, ClickableImageLabel
from core.theme_manager import get_theme_manager


class ProfileItem(QFrame):
    """Individual profile card with selection states and context menus"""
    clicked = Signal(str)
    edit_requested = Signal(str)
    duplicate_requested = Signal(str)
    delete_requested = Signal(str)
    
    def __init__(self, name, profile_data=None, is_add_button=False, card_type="success", parent=None):
        super().__init__(parent)
        self.name = name
        self.profile_data = profile_data or {}
        self.is_add_button = is_add_button
        self.card_type = card_type  # "neutral", "success", or "danger"
        self.selected = False
        self._is_hovered = False
        
        # Get theme manager
        self.theme_manager = get_theme_manager()
        
        self.setFixedSize(120, 140)
        self.setCursor(Qt.PointingHandCursor)
        
        # Layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        
        # Image
        self.image_label = ClickableImageLabel((100, 100))
        self.image_label.setScaledContents(True)
        self.update_image()
        layout.addWidget(self.image_label, alignment=Qt.AlignCenter)
        
        # Name label
        self.name_label = ThemedLabel(name)
        self.name_label.setAlignment(Qt.AlignCenter)
        self.name_label.setWordWrap(True)
        layout.addWidget(self.name_label)
        
        # Set initial style
        self.update_style()
        
        # Connect to theme changes - both for style and image
        self.theme_manager.theme_changed.connect(self.update_style)
        self.theme_manager.theme_changed.connect(self.update_image)
    
    def update_image(self):
        """Update the displayed image"""
        # Get colors from theme for placeholder
        colors = self.theme_manager.get_profile_card_colors(self.card_type)
        image_bg = colors.get('card_image_background', '#282a36')
        text_color = self.theme_manager.get_color('text.primary')
        
        if self.is_add_button:
            # Add button placeholder with theme colors
            pixmap = PlaceholderPixmap.create_add_button((100, 100), image_bg, text_color)
        elif self.profile_data.get("image"):
            # Load profile image
            loaded_pixmap = QPixmap(self.profile_data["image"])
            if not loaded_pixmap.isNull():
                pixmap = loaded_pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            else:
                pixmap = PlaceholderPixmap.create_file_icon((100, 100), icon="📄", background_color=image_bg, text_color=text_color)
        else:
            # Default profile icon with theme colors
            pixmap = PlaceholderPixmap.create_file_icon((100, 100), icon="📄", background_color=image_bg, text_color=text_color)
        
        self.image_label.setPixmap(pixmap)
    
    def set_selected(self, selected):
        """Update selection state"""
        self.selected = selected
        self.update_style()
    
    def update_style(self):
        """Apply styling based on current state using theme colors"""
        # Get colors from theme
        colors = self.theme_manager.get_profile_card_colors(self.card_type)
        card_styles = self.theme_manager.get_style('cards')
        
        # Get border radius and width from theme
        border_radius = card_styles.get('border_radius', 4) if card_styles else 4
        border_width = card_styles.get('border_width', 2) if card_styles else 2
        
        if self.selected:
            # Selected state
            bg_color = colors['selected']['background']
            border_color = colors['selected']['border']
            border_width = 3  # Thicker border for selected
        elif self._is_hovered:
            # Hover state
            bg_color = colors['hovered']['background']
            border_color = colors['hovered']['border']
        else:
            # Normal state
            bg_color = colors['normal']['background']
            border_color = colors['normal']['border']
        
        # Get text color for label from theme
        text_color = self.theme_manager.get_color('text.primary')
        
        # Get image background color from theme
        image_bg = colors.get('card_image_background', '#282a36')
        
        self.setStyleSheet(f"""
            ProfileItem {{
                background-color: {bg_color};
                border: {border_width}px solid {border_color};
                border-radius: {border_radius}px;
            }}
        """)
        
        # Update label color
        self.name_label.setStyleSheet(f"color: {text_color}; background: transparent;")
        
        # Update image label background
        self.image_label.setStyleSheet(f"""
            ClickableImageLabel {{
                background-color: {image_bg};
                border: 1px solid {border_color};
                border-radius: 4px;
            }}
        """)
        
        self.update()
    
    def enterEvent(self, event):
        """Handle mouse enter"""
        if not self.selected:
            self._is_hovered = True
            self.update_style()
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        """Handle mouse leave"""
        self._is_hovered = False
        self.update_style()
        super().leaveEvent(event)
    
    def mousePressEvent(self, event):
        """Handle mouse clicks"""
        if event.button() == Qt.LeftButton:
            self.clicked.emit(self.name)
        elif event.button() == Qt.RightButton and not self.is_add_button:
            # Show context menu for non-add buttons
            self.show_context_menu(event.globalPos())
    
    def show_context_menu(self, pos):
        """Show right-click context menu"""
        menu = ThemedMenu(self)
        
        edit_action = menu.addAction("Edit")
        duplicate_action = menu.addAction("Duplicate")
        menu.addSeparator()
        delete_action = menu.addAction("Delete")
        
        action = menu.exec(pos)
        
        if action == edit_action:
            self.edit_requested.emit(self.name)
        elif action == duplicate_action:
            self.duplicate_requested.emit(self.name)
        elif action == delete_action:
            self.delete_requested.emit(self.name)

