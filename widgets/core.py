"""
Core Widgets Module

Consolidated module for themed and simple atomic widgets.
"""

from PySide6.QtWidgets import (QPushButton, QLineEdit, QTextEdit, QSpinBox, QGroupBox,
                             QScrollArea, QSplitter, QLabel, QCheckBox, QRadioButton,
                             QListWidget, QMenu, QSizePolicy)
from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtGui import QFont, QPixmap, QPainter, QColor


# MARK: - Themed Widgets (Base Styles)

class PurpleButton(QPushButton):
    """Standard purple theme button - most common button type"""
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.setStyleSheet("""
            QPushButton {
                background-color: #1d1f28;
                color: #BB86FC;
                border: 2px solid #BB86FC;
                border-radius: 4px;
                padding: 6px 12px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #000000;
                color: #9965DA;
                border: 2px solid #9965DA;
            }
            QPushButton:pressed {
                background-color: #BB86FC;
                color: #1d1f28;
            }
            QPushButton:disabled {
                background-color: #1d1f28;
                color: #6f779a;
                border: 2px solid #6f779a;
            }
        """)


class GreenButton(QPushButton):
    """Green success/next buttons"""
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.setStyleSheet("""
            QPushButton {
                background-color: #1d1f28;
                color: #23c87b;
                border: 2px solid #23c87b;
                border-radius: 4px;
                padding: 6px 12px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #000000;
                color: #1a945b;
                border: 2px solid #1a945b;
            }
            QPushButton:pressed {
                background-color: #23c87b;
                color: #1d1f28;
            }
            QPushButton:disabled {
                background-color: #1d1f28;
                color: #6f779a;
                border: 2px solid #6f779a;
            }
        """)


class BlueButton(QPushButton):
    """Blue project buttons"""
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.setStyleSheet("""
            QPushButton {
                background-color: #1d1f28;
                color: #00c4fe;
                border: 2px solid #00c4fe;
                border-radius: 4px;
                padding: 6px 12px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #000000;
                color: #0099cc;
                border: 2px solid #0099cc;
            }
            QPushButton:pressed {
                background-color: #00c4fe;
                color: #1d1f28;
            }
        """)


class OrangeButton(QPushButton):
    """Orange export buttons"""
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.setStyleSheet("""
            QPushButton {
                background-color: #1d1f28;
                color: #ff8c00;
                border: 2px solid #ff8c00;
                border-radius: 4px;
                padding: 6px 12px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #000000;
                color: #e67300;
                border: 2px solid #e67300;
            }
            QPushButton:pressed {
                background-color: #ff8c00;
                color: #1d1f28;
            }
        """)


class ThemedLineEdit(QLineEdit):
    """Dark themed line edit with focus states"""
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
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
            QLineEdit:disabled {
                background-color: #0d0f18;
                color: #6f779a;
                border: 1px solid #4a506a;
            }
        """)


class ThemedTextEdit(QTextEdit):
    """Dark themed text edit"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QTextEdit {
                background-color: #1d1f28;
                color: #ffffff;
                border: 1px solid #6f779a;
                border-radius: 4px;
                padding: 4px;
            }
            QTextEdit:focus {
                border: 1px solid #BB86FC;
            }
        """)


class ThemedSpinBox(QSpinBox):
    """Dark themed spin box with custom arrows"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QSpinBox {
                background-color: #1d1f28;
                color: #ffffff;
                border: 1px solid #6f779a;
                border-radius: 4px;
                padding: 4px;
            }
            QSpinBox::up-button, QSpinBox::down-button {
                background-color: #44475c;
                border: none;
                width: 16px;
            }
            QSpinBox::up-button:hover, QSpinBox::down-button:hover {
                background-color: #6f779a;
            }
        """)


class ThemedGroupBox(QGroupBox):
    """Dark themed group box with border"""
    def __init__(self, title="", parent=None):
        super().__init__(title, parent)
        self.setStyleSheet("""
            QGroupBox {
                border: 2px solid #44475c;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
                color: #ffffff;
                font-weight: bold;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)


class ThemedScrollArea(QScrollArea):
    """Dark themed scroll area with custom scrollbars"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QScrollArea {
                background-color: #1d1f28;
                border: 1px solid #6f779a;
                border-radius: 4px;
            }
            QScrollArea QScrollBar:vertical {
                background-color: #1d1f28;
                width: 12px;
                margin: 0px;
            }
            QScrollArea QScrollBar::handle:vertical {
                background-color: #6f779a;
                min-height: 20px;
                border-radius: 6px;
            }
            QScrollArea QScrollBar::add-line:vertical, QScrollArea QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QScrollArea QScrollBar:horizontal {
                background-color: #1d1f28;
                height: 12px;
                margin: 0px;
            }
            QScrollArea QScrollBar::handle:horizontal {
                background-color: #6f779a;
                min-width: 20px;
                border-radius: 6px;
            }
            QScrollArea QScrollBar::add-line:horizontal, QScrollArea QScrollBar::sub-line:horizontal {
                width: 0px;
            }
        """)


class ThemedSplitter(QSplitter):
    """Custom splitter handles"""
    def __init__(self, orientation=Qt.Horizontal, parent=None):
        super().__init__(orientation, parent)
        self.setStyleSheet("""
            QSplitter::handle {
                background-color: #44475c;
                width: 4px;
            }
            QSplitter::handle:horizontal {
                width: 4px;
            }
            QSplitter::handle:vertical {
                height: 4px;
            }
            QSplitter::handle:hover {
                background-color: #BB86FC;
            }
        """)


class ThemedLabel(QLabel):
    """White text labels"""
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.setStyleSheet("""
            QLabel {
                color: #ffffff;
                background-color: transparent;
            }
        """)


class ThemedCheckBox(QCheckBox):
    """Custom checkbox with purple accent"""
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.setStyleSheet("""
            QCheckBox {
                color: #ffffff;
            }
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
                border: 2px solid #6f779a;
                background-color: #1d1f28;
                border-radius: 3px;
            }
            QCheckBox::indicator:checked {
                background-color: #23c87b;
                border-color: #23c87b;
            }
        """)


class ThemedRadioButton(QRadioButton):
    """Custom radio button with purple accent"""
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.setStyleSheet("""
            QRadioButton {
                color: #ffffff;
            }
            QRadioButton::indicator {
                width: 16px;
                height: 16px;
                border: 2px solid #6f779a;
                background-color: #1d1f28;
                border-radius: 8px;
            }
            QRadioButton::indicator:checked {
                background-color: #23c87b;
                border-color: #23c87b;
            }
        """)


class ThemedListWidget(QListWidget):
    """Dark themed list widget"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QListWidget {
                background-color: #1d1f28;
                color: #ffffff;
                border: 1px solid #6f779a;
                border-radius: 4px;
                padding: 4px;
                outline: none;
            }
            QListWidget::item {
                background-color: #44475c;
                border: 1px solid #6f779a;
                border-radius: 3px;
                padding: 6px;
                margin: 2px;
            }
            QListWidget::item:selected {
                background-color: #BB86FC;
                color: #1d1f28;
                border: 1px solid #BB86FC;
            }
            QListWidget::item:hover {
                background-color: #6f779a;
                border: 1px solid #8b95c0;
            }
        """)


class ThemedMenu(QMenu):
    """Dark themed context menu"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QMenu {
                background-color: #1d1f28;
                color: #ffffff;
                border: 1px solid #6f779a;
                border-radius: 4px;
            }
            QMenu::item {
                background-color: transparent;
                padding: 6px 16px;
            }
            QMenu::item:selected {
                background-color: #6f779a;
            }
        """)


# MARK: - Simple Widgets (Interactive)

class ClickableLabel(QLabel):
    """Label that acts like a button/link with hover effects"""
    clicked = Signal()
    
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet("""
            QLabel {
                color: #BB86FC;
                text-decoration: underline;
                background-color: transparent;
            }
            QLabel:hover {
                color: #9965DA;
            }
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
        self.setScaledContents(False)
        self.setAlignment(Qt.AlignCenter)
        self.setWordWrap(True)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setMinimumSize(200, 200)  # Minimum reasonable size
        self._pixmap = None
        self._placeholder_text = ""
        
        # Apply preview styling
        self.setStyleSheet("""
            QLabel {
                background-color: #44475c;
                border: 2px solid #6f779a;
                border-radius: 4px;
                color: #bdbdc0;
                padding: 10px;
            }
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
        self.setFixedSize(*size)
        self.setAlignment(Qt.AlignCenter)
        self.setCursor(Qt.PointingHandCursor)
        self.setScaledContents(False)
        self.setStyleSheet("""
            ClickableImageLabel {
                background-color: #44475c;
                border: 2px solid #6f779a;
                border-radius: 4px;
            }
            ClickableImageLabel:hover {
                background-color: #3a3d4d;
                border: 2px solid #BB86FC;
            }
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
    def create_profile_placeholder(size=(150, 150)):
        """Create profile image placeholder"""
        return PlaceholderPixmap.create(size, "Profile Image")
    
    @staticmethod
    def create_type_placeholder(size=(80, 80)):
        """Create type image placeholder"""
        return PlaceholderPixmap.create(size, "📐")
    
    @staticmethod
    def create_add_button(size=(80, 80)):
        """Create add button placeholder"""
        return PlaceholderPixmap.create(size, "+")
    
    @staticmethod
    def create_file_icon(size=(60, 60), icon="📄"):
        """Create file icon placeholder"""
        return PlaceholderPixmap.create(size, icon)
