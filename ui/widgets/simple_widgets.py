"""
Simple Widgets Module

Updated with ScaledPreviewLabel for proper aspect ratio scaling.
"""

from PySide6.QtWidgets import QLabel, QLineEdit, QSizePolicy
from PySide6.QtCore import Signal, Qt, QSize
from PySide6.QtGui import QPixmap, QPainter, QColor, QFont
from .themed_widgets import ThemedLineEdit
from core.theme_manager import get_theme_manager


class ClickableLabel(QLabel):
    """Label that acts like a button/link with hover effects"""
    clicked = Signal()
    
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.theme_manager = get_theme_manager()
        self.setCursor(Qt.PointingHandCursor)
        self.update_theme_colors()
        # Connect to theme changes
        self.theme_manager.theme_changed.connect(self.update_theme_colors)
    
    def update_theme_colors(self):
        """Update colors from theme"""
        link_color = self.theme_manager.get_color('text.links')
        accent = self.theme_manager.get_color('accents.primary')
        
        self.setStyleSheet(f"""
            QLabel {{
                color: {link_color};
                text-decoration: underline;
                background-color: transparent;
            }}
            QLabel:hover {{
                color: {accent};
            }}
        """)
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)


class ScaledImageLabel(QLabel):
    """Image label that maintains aspect ratio when scaling to fill available space"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setScaledContents(False)
        self.setAlignment(Qt.AlignCenter)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self._pixmap = None
    
    def setPixmap(self, pixmap):
        """Set pixmap and store original for scaling"""
        self._pixmap = pixmap
        self.updatePixmap()
    
    def updatePixmap(self):
        """Update displayed pixmap based on current size"""
        if self._pixmap and not self._pixmap.isNull():
            scaled = self._pixmap.scaled(
                self.size(), 
                Qt.KeepAspectRatio, 
                Qt.SmoothTransformation
            )
            super().setPixmap(scaled)
    
    def resizeEvent(self, event):
        """Handle resize to update pixmap scaling"""
        super().resizeEvent(event)
        self.updatePixmap()


class ScaledPreviewLabel(QLabel):
    """Preview label that scales to maximum available space while maintaining aspect ratio"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.theme_manager = get_theme_manager()
        self.setScaledContents(False)
        self.setAlignment(Qt.AlignCenter)
        self.setWordWrap(True)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setMinimumSize(200, 200)  # Minimum reasonable size
        self._pixmap = None
        self._placeholder_text = ""
        
        # Apply theme colors
        self.update_theme_colors()
        # Connect to theme changes
        self.theme_manager.theme_changed.connect(self.update_theme_colors)
    
    def update_theme_colors(self):
        """Update colors from theme"""
        preview_colors = self.theme_manager.get_image_preview_colors()
        text_color = self.theme_manager.get_color('text.secondary')
        
        self.setStyleSheet(f"""
            QLabel {{
                background-color: {preview_colors['background']};
                border: 2px solid {preview_colors['border_inactive']};
                border-radius: 4px;
                color: {text_color};
                padding: 10px;
            }}
        """)
    
    def setPixmap(self, pixmap):
        """Set pixmap and store original for scaling"""
        if pixmap and not pixmap.isNull():
            self._pixmap = pixmap
            self._placeholder_text = ""  # Clear placeholder when setting valid image
        else:
            # Invalid pixmap, clear it
            self._pixmap = None
        self.updateDisplay()
    
    def setText(self, text):
        """Set placeholder text (clears any pixmap)"""
        self._placeholder_text = text or ""  # Handle None text
        self._pixmap = None
        self.updateDisplay()
    
    def updateDisplay(self):
        """Update displayed content based on current size"""
        if self._pixmap and not self._pixmap.isNull():
            # Scale pixmap to fit available space while maintaining aspect ratio
            scaled = self._pixmap.scaled(
                self.size(), 
                Qt.KeepAspectRatio, 
                Qt.SmoothTransformation
            )
            super().setPixmap(scaled)
            super().setText("")  # Clear any text
        else:
            # Show placeholder text
            super().setPixmap(QPixmap())  # Clear any pixmap
            super().setText(self._placeholder_text)
    
    def resizeEvent(self, event):
        """Handle resize to update display"""
        super().resizeEvent(event)
        self.updateDisplay()
    
    def paintEvent(self, event):
        """Custom paint to handle text centering properly"""
        if self._pixmap and not self._pixmap.isNull():
            # Let QLabel handle pixmap painting with proper scaling
            super().paintEvent(event)
        else:
            # Let QLabel handle background and placeholder text drawing once
            super().paintEvent(event)
    
    def clear(self):
        """Clear both pixmap and text"""
        self._pixmap = None
        self._placeholder_text = ""
        self.updateDisplay()
    
    def hasValidImage(self):
        """Check if label has a valid image"""
        return self._pixmap is not None and not self._pixmap.isNull()
    
    def hasText(self):
        """Check if label has placeholder text"""
        return bool(self._placeholder_text)


class ClickableImageLabel(QLabel):
    """Image selector that forwards both left and right clicks to parent"""
    clicked = Signal()
    
    def __init__(self, size=(100, 100), parent=None):
        super().__init__(parent)
        self.theme_manager = get_theme_manager()
        self.setFixedSize(*size)
        self.setAlignment(Qt.AlignCenter)
        self.setCursor(Qt.PointingHandCursor)
        self.setScaledContents(False)
        
        # Apply theme colors
        self.update_theme_colors()
        # Connect to theme changes
        self.theme_manager.theme_changed.connect(self.update_theme_colors)
    
    def update_theme_colors(self):
        """Update colors from theme"""
        preview_colors = self.theme_manager.get_image_preview_colors()
        
        self.setStyleSheet(f"""
            ClickableImageLabel {{
                background-color: {preview_colors['background']};
                border: 2px solid {preview_colors['border_inactive']};
                border-radius: 4px;
            }}
            ClickableImageLabel:hover {{
                background-color: {preview_colors['background']};
                border: 2px solid {preview_colors['border_active']};
            }}
        """)
        
    def mousePressEvent(self, event):
        """Forward both left and right clicks to parent"""
        if event.button() == Qt.LeftButton:
            self.clicked.emit()
        
        # Forward the event to parent so it can handle right-clicks too
        # Convert the event position to parent coordinates
        parent_pos = self.mapToParent(event.pos())
        new_event = type(event)(
            event.type(),
            parent_pos,
            event.globalPos(),
            event.button(),
            event.buttons(),
            event.modifiers()
        )
        
        # Send the event to the parent
        if self.parent():
            self.parent().mousePressEvent(new_event)


class ErrorLineEdit(ThemedLineEdit):
    """LineEdit with red border for validation errors"""
    
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self._has_error = False
    
    def set_error(self, has_error):
        """Set error state and update styling"""
        self._has_error = has_error
        if has_error:
            self.setStyleSheet("""
                QLineEdit {
                    background-color: #1d1f28;
                    color: #ffffff;
                    border: 2px solid #ff4444;
                    border-radius: 4px;
                    padding: 4px;
                }
                QLineEdit:focus {
                    border: 2px solid #ff4444;
                }
            """)
        else:
            # Reset to normal themed style
            self.setStyleSheet("""
                QLineEdit {
                    background-color: #1d1f28;
                    color: #ffffff;
                    border: 1px solid #6f779a;
                    border-radius: 4px;
                    padding: 4px;
                }
                QLineEdit:focus {
                    border: 1px solid #BB86FC;
                }
            """)
    
    def has_error(self):
        """Check if widget has error state"""
        return self._has_error


class PlaceholderPixmap:
    """Utility class for creating placeholder pixmaps with text/icons"""
    
    @staticmethod
    def create(size, text="", background_color="#44475c", text_color="#bdbdc0"):
        """Create a placeholder pixmap with text"""
        pixmap = QPixmap(*size)
        pixmap.fill(QColor(background_color))
        
        if text:
            painter = QPainter(pixmap)
            painter.setPen(QColor(text_color))
            painter.drawText(pixmap.rect(), Qt.AlignCenter, text)
            painter.end()
        
        return pixmap
    
    @staticmethod
    def create_profile_placeholder(size=(150, 150), background_color="#44475c", text_color="#bdbdc0"):
        """Create profile image placeholder"""
        return PlaceholderPixmap.create(size, "Profile Image", background_color, text_color)
    
    @staticmethod
    def create_type_placeholder(size=(80, 80), background_color="#44475c", text_color="#bdbdc0"):
        """Create type image placeholder"""
        return PlaceholderPixmap.create(size, "📐", background_color, text_color)
    
    @staticmethod
    def create_add_button(size=(80, 80), background_color="#44475c", text_color="#bdbdc0"):
        """Create add button placeholder"""
        return PlaceholderPixmap.create(size, "+", background_color, text_color)
    
    @staticmethod
    def create_file_icon(size=(60, 60), icon="📄", background_color="#44475c", text_color="#bdbdc0"):
        """Create file icon placeholder"""
        return PlaceholderPixmap.create(size, icon, background_color, text_color)