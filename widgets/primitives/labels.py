from PySide6.QtWidgets import QLabel, QSizePolicy
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap
from widgets.mixins import ThemedWidgetMixin
from core.theme_manager import get_theme_manager

class ThemedLabel(QLabel, ThemedWidgetMixin):
    """Base themed label"""
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        ThemedWidgetMixin.__init__(self)

class ClickableLabel(ThemedLabel):
    """Label that acts like a button/link with hover effects"""
    clicked = Signal()
    
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.setCursor(Qt.PointingHandCursor)
        self.setProperty("class", "link")
        # Ensure style handles this, or use on_theme_changed if stylesheet lacks support
        
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)
        
    def on_theme_changed(self, theme_name):
        # Fallback manual styling if needed, but prefer stylesheet
        tm = get_theme_manager()
        link_color = tm.get_color("text.links")
        self.setStyleSheet(f"""
            QLabel {{
                color: {link_color};
                text-decoration: underline;
                background-color: transparent;
            }}
            QLabel:hover {{
                color: {tm.get_color("accents.primary")};
            }}
        """)

class ScaledImageLabel(QLabel):
    """Image label that maintains aspect ratio when scaling"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setScaledContents(False)
        self.setAlignment(Qt.AlignCenter)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self._pixmap = None
    
    def setPixmap(self, pixmap):
        self._pixmap = pixmap
        self.updatePixmap()
    
    def updatePixmap(self):
        if self._pixmap and not self._pixmap.isNull():
            scaled = self._pixmap.scaled(
                self.size(), 
                Qt.KeepAspectRatio, 
                Qt.SmoothTransformation
            )
            super().setPixmap(scaled)
    
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.updatePixmap()

class ClickableImageLabel(ScaledImageLabel, ThemedWidgetMixin):
    """Image selector with theme support"""
    clicked = Signal()
    
    def __init__(self, size=(100, 100), parent=None):
        super().__init__(parent)
        ThemedWidgetMixin.__init__(self)
        self.setFixedSize(*size)
        self.setCursor(Qt.PointingHandCursor)
        self.update_style()
        
    def on_theme_changed(self, theme_name):
        self.update_style()
        
    def update_style(self):
        tm = get_theme_manager()
        bg = tm.get_color("backgrounds.tertiary")
        border = tm.get_color("borders.inactive")
        hover_border = tm.get_color("accents.primary")
        hover_bg = tm.get_color("buttons.neutral.hovered.background") # Approximation
        
        self.setStyleSheet(f"""
            ClickableImageLabel {{
                background-color: {bg};
                border: 2px solid {border};
                border-radius: 4px;
            }}
            ClickableImageLabel:hover {{
                background-color: {hover_bg};
                border: 2px solid {hover_border};
            }}
        """)
        
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()
        
        # Forward event to parent for context menus
        if self.parent():
            parent_pos = self.mapToParent(event.pos())
            new_event = type(event)(
                event.type(),
                parent_pos,
                event.globalPos(),
                event.button(),
                event.buttons(),
                event.modifiers()
            )
            self.parent().mousePressEvent(new_event)

class ScaledPreviewLabel(ScaledImageLabel, ThemedWidgetMixin):
    """Preview label with theme support"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        ThemedWidgetMixin.__init__(self)
        self.setWordWrap(True)
        self.setMinimumSize(200, 200)
        self._placeholder_text = ""
        self.update_style()
        
    def on_theme_changed(self, theme_name):
        self.update_style()
        
    def update_style(self):
        tm = get_theme_manager()
        bg = tm.get_color("backgrounds.tertiary")
        border = tm.get_color("borders.inactive")
        text_color = tm.get_color("text.secondary")
        
        self.setStyleSheet(f"""
            QLabel {{
                background-color: {bg};
                border: 2px solid {border};
                border-radius: 4px;
                color: {text_color};
                padding: 10px;
            }}
        """)

    def setText(self, text):
        self._placeholder_text = text or ""
        self._pixmap = None
        self.updateDisplay()
        
    def updateDisplay(self):
        if self._pixmap and not self._pixmap.isNull():
            super().updatePixmap()
            QLabel.setText(self, "") 
        else:
            QLabel.setPixmap(self, QPixmap())
            QLabel.setText(self, self._placeholder_text)
            
    def setPixmap(self, pixmap):
        if pixmap and not pixmap.isNull():
            self._pixmap = pixmap
            self._placeholder_text = ""
        else:
            self._pixmap = None
        self.updateDisplay()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.updateDisplay()
