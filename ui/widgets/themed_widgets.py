"""
Themed Widgets Module

Theme-aware widgets that automatically update when theme changes.
Integrates with ThemeManager for dynamic styling.
"""

from PySide6.QtWidgets import (QPushButton, QLineEdit, QTextEdit, QSpinBox, QDoubleSpinBox,
                             QGroupBox, QScrollArea, QSplitter, QLabel, QCheckBox, 
                             QRadioButton, QListWidget, QMenu)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from core.theme_manager import ThemeManager


class ThemedButton(QPushButton):
    """Base themed button that updates with theme changes"""
    
    def __init__(self, text="", button_type="primary", parent=None):
        super().__init__(text, parent)
        self.button_type = button_type
        self._theme_manager = ThemeManager()
        
        # Connect to theme changes
        self._theme_manager.theme_changed.connect(self.apply_theme)
        self.apply_theme()
    
    def apply_theme(self):
        """Apply theme styling to button"""
        if not self._theme_manager.current_theme:
            return
        
        theme = self._theme_manager.current_theme
        btn_colors = theme['buttons'].get(self.button_type, theme['buttons']['primary'])
        styles = theme.get('control_styles', {}).get('buttons', {})
        
        border_radius = styles.get('border_radius', 4)
        padding_h = styles.get('padding_horizontal', 12)
        padding_v = styles.get('padding_vertical', 6)
        font_size = styles.get('font_size', 10)
        
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {btn_colors['normal']['background']};
                color: {btn_colors['normal']['text']};
                border: 2px solid {btn_colors['normal']['outline']};
                border-radius: {border_radius}px;
                padding: {padding_v}px {padding_h}px;
                font-size: {font_size}pt;
            }}
            QPushButton:hover {{
                background-color: {btn_colors['hovered']['background']};
                color: {btn_colors['hovered']['text']};
                border: 2px solid {btn_colors['hovered']['outline']};
            }}
            QPushButton:pressed {{
                background-color: {btn_colors['clicked']['background']};
                color: {btn_colors['clicked']['text']};
                border: 2px solid {btn_colors['clicked']['outline']};
            }}
            QPushButton:disabled {{
                background-color: {btn_colors['disabled']['background']};
                color: {btn_colors['disabled']['text']};
                border: 2px solid {btn_colors['disabled']['outline']};
            }}
        """)


# Convenience button classes for common types
class PurpleButton(ThemedButton):
    """Purple primary button"""
    def __init__(self, text="", parent=None):
        super().__init__(text, button_type="primary", parent=parent)


class GreenButton(ThemedButton):
    """Green success button"""
    def __init__(self, text="", parent=None):
        super().__init__(text, button_type="success", parent=parent)


class BlueButton(ThemedButton):
    """Blue secondary button"""
    def __init__(self, text="", parent=None):
        super().__init__(text, button_type="secondary", parent=parent)


class OrangeButton(ThemedButton):
    """Orange warning/export button"""
    def __init__(self, text="", parent=None):
        super().__init__(text, button_type="export", parent=parent)


class ThemedLineEdit(QLineEdit):
    """Themed line edit with auto-updating styles"""
    
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self._theme_manager = ThemeManager()
        self._theme_manager.theme_changed.connect(self.apply_theme)
        self.apply_theme()
    
    def apply_theme(self):
        """Apply theme styling"""
        if not self._theme_manager.current_theme:
            return
        
        theme = self._theme_manager.current_theme
        styles = theme.get('control_styles', {}).get('inputs', {})
        
        bg_input = theme['backgrounds']['input']
        text_primary = theme['text']['primary']
        text_disabled = theme['text']['disabled']
        border_inactive = theme['borders']['inactive']
        border_active = theme['borders']['active']
        
        border_radius = styles.get('border_radius', 4)
        padding_h = styles.get('padding_horizontal', 8)
        padding_v = styles.get('padding_vertical', 4)
        focus_border = styles.get('focus_border_width', 2)
        
        self.setStyleSheet(f"""
            QLineEdit {{
                background-color: {bg_input};
                color: {text_primary};
                border: 1px solid {border_inactive};
                border-radius: {border_radius}px;
                padding: {padding_v}px {padding_h}px;
            }}
            QLineEdit:focus {{
                border: {focus_border}px solid {border_active};
            }}
            QLineEdit:disabled {{
                background-color: {theme['backgrounds']['tertiary']};
                color: {text_disabled};
            }}
        """)


class ThemedTextEdit(QTextEdit):
    """Themed text edit"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._theme_manager = ThemeManager()
        self._theme_manager.theme_changed.connect(self.apply_theme)
        self.apply_theme()
    
    def apply_theme(self):
        if not self._theme_manager.current_theme:
            return
        
        theme = self._theme_manager.current_theme
        styles = theme.get('control_styles', {}).get('inputs', {})
        
        self.setStyleSheet(f"""
            QTextEdit {{
                background-color: {theme['backgrounds']['input']};
                color: {theme['text']['primary']};
                border: 1px solid {theme['borders']['inactive']};
                border-radius: {styles.get('border_radius', 4)}px;
                padding: {styles.get('padding_vertical', 4)}px;
            }}
            QTextEdit:focus {{
                border: {styles.get('focus_border_width', 2)}px solid {theme['borders']['active']};
            }}
        """)


class ThemedSpinBox(QSpinBox):
    """Themed spin box"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._theme_manager = ThemeManager()
        self._theme_manager.theme_changed.connect(self.apply_theme)
        self.apply_theme()
    
    def apply_theme(self):
        if not self._theme_manager.current_theme:
            return
        
        theme = self._theme_manager.current_theme
        styles = theme.get('control_styles', {}).get('inputs', {})
        
        self.setStyleSheet(f"""
            QSpinBox {{
                background-color: {theme['backgrounds']['input']};
                color: {theme['text']['primary']};
                border: 1px solid {theme['borders']['inactive']};
                border-radius: {styles.get('border_radius', 4)}px;
                padding: {styles.get('padding_vertical', 4)}px {styles.get('padding_horizontal', 8)}px;
            }}
            QSpinBox:focus {{
                border: {styles.get('focus_border_width', 2)}px solid {theme['borders']['active']};
            }}
            QSpinBox::up-button, QSpinBox::down-button {{
                background-color: {theme['backgrounds']['tertiary']};
                border: none;
                width: 16px;
            }}
            QSpinBox::up-button:hover, QSpinBox::down-button:hover {{
                background-color: {theme['backgrounds']['secondary']};
            }}
        """)


class ThemedDoubleSpinBox(QDoubleSpinBox):
    """Themed double spin box"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._theme_manager = ThemeManager()
        self._theme_manager.theme_changed.connect(self.apply_theme)
        self.apply_theme()
    
    def apply_theme(self):
        if not self._theme_manager.current_theme:
            return
        
        theme = self._theme_manager.current_theme
        styles = theme.get('control_styles', {}).get('inputs', {})
        
        self.setStyleSheet(f"""
            QDoubleSpinBox {{
                background-color: {theme['backgrounds']['input']};
                color: {theme['text']['primary']};
                border: 1px solid {theme['borders']['inactive']};
                border-radius: {styles.get('border_radius', 4)}px;
                padding: {styles.get('padding_vertical', 4)}px {styles.get('padding_horizontal', 8)}px;
            }}
            QDoubleSpinBox:focus {{
                border: {styles.get('focus_border_width', 2)}px solid {theme['borders']['active']};
            }}
            QDoubleSpinBox::up-button, QDoubleSpinBox::down-button {{
                background-color: {theme['backgrounds']['tertiary']};
                border: none;
                width: 16px;
            }}
            QDoubleSpinBox::up-button:hover, QDoubleSpinBox::down-button:hover {{
                background-color: {theme['backgrounds']['secondary']};
            }}
        """)


class ThemedGroupBox(QGroupBox):
    """Themed group box"""
    
    def __init__(self, title="", parent=None):
        super().__init__(title, parent)
        self._theme_manager = ThemeManager()
        self._theme_manager.theme_changed.connect(self.apply_theme)
        self.apply_theme()
    
    def apply_theme(self):
        if not self._theme_manager.current_theme:
            return
        
        theme = self._theme_manager.current_theme
        styles = theme.get('control_styles', {}).get('cards', {})
        
        self.setStyleSheet(f"""
            QGroupBox {{
                border: 2px solid {theme['borders']['inactive']};
                border-radius: {styles.get('border_radius', 8)}px;
                margin-top: 12px;
                padding: {styles.get('padding', 10)}px;
                background-color: {theme['backgrounds']['secondary']};
                color: {theme['text']['primary']};
                font-weight: bold;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }}
        """)


class ThemedLabel(QLabel):
    """Themed label"""
    
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self._theme_manager = ThemeManager()
        self._theme_manager.theme_changed.connect(self.apply_theme)
        self.apply_theme()
    
    def apply_theme(self):
        if not self._theme_manager.current_theme:
            return
        
        theme = self._theme_manager.current_theme
        styles = theme.get('control_styles', {}).get('labels', {})
        
        self.setStyleSheet(f"""
            QLabel {{
                color: {theme['text']['primary']};
                background: transparent;
                font-size: {styles.get('font_size', 9)}pt;
            }}
        """)


class ThemedCheckBox(QCheckBox):
    """Themed checkbox"""
    
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self._theme_manager = ThemeManager()
        self._theme_manager.theme_changed.connect(self.apply_theme)
        self.apply_theme()
    
    def apply_theme(self):
        if not self._theme_manager.current_theme:
            return
        
        theme = self._theme_manager.current_theme
        
        self.setStyleSheet(f"""
            QCheckBox {{
                color: {theme['text']['primary']};
                spacing: 5px;
            }}
            QCheckBox::indicator {{
                width: 16px;
                height: 16px;
                border: 1px solid {theme['borders']['inactive']};
                border-radius: 3px;
                background-color: {theme['backgrounds']['input']};
            }}
            QCheckBox::indicator:checked {{
                background-color: {theme['accents']['primary']};
                border-color: {theme['accents']['primary']};
            }}
            QCheckBox::indicator:hover {{
                border-color: {theme['borders']['active']};
            }}
        """)


class ThemedRadioButton(QRadioButton):
    """Themed radio button"""
    
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self._theme_manager = ThemeManager()
        self._theme_manager.theme_changed.connect(self.apply_theme)
        self.apply_theme()
    
    def apply_theme(self):
        if not self._theme_manager.current_theme:
            return
        
        theme = self._theme_manager.current_theme
        
        self.setStyleSheet(f"""
            QRadioButton {{
                color: {theme['text']['primary']};
                spacing: 5px;
            }}
            QRadioButton::indicator {{
                width: 16px;
                height: 16px;
                border: 1px solid {theme['borders']['inactive']};
                border-radius: 8px;
                background-color: {theme['backgrounds']['input']};
            }}
            QRadioButton::indicator:checked {{
                background-color: {theme['accents']['primary']};
                border-color: {theme['accents']['primary']};
            }}
            QRadioButton::indicator:hover {{
                border-color: {theme['borders']['active']};
            }}
        """)


class ThemedScrollArea(QScrollArea):
    """Themed scroll area"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._theme_manager = ThemeManager()
        self._theme_manager.theme_changed.connect(self.apply_theme)
        self.apply_theme()
    
    def apply_theme(self):
        if not self._theme_manager.current_theme:
            return
        
        theme = self._theme_manager.current_theme
        
        self.setStyleSheet(f"""
            QScrollArea {{
                background-color: {theme['backgrounds']['secondary']};
                border: 1px solid {theme['borders']['inactive']};
            }}
        """)


class ThemedSplitter(QSplitter):
    """Themed splitter"""
    
    def __init__(self, orientation=Qt.Horizontal, parent=None):
        super().__init__(orientation, parent)
        self._theme_manager = ThemeManager()
        self._theme_manager.theme_changed.connect(self.apply_theme)
        self.apply_theme()
    
    def apply_theme(self):
        if not self._theme_manager.current_theme:
            return
        
        theme = self._theme_manager.current_theme
        
        self.setStyleSheet(f"""
            QSplitter::handle {{
                background-color: {theme['borders']['inactive']};
            }}
            QSplitter::handle:hover {{
                background-color: {theme['borders']['active']};
            }}
        """)


class ThemedListWidget(QListWidget):
    """Themed list widget"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._theme_manager = ThemeManager()
        self._theme_manager.theme_changed.connect(self.apply_theme)
        self.apply_theme()
    
    def apply_theme(self):
        if not self._theme_manager.current_theme:
            return
        
        theme = self._theme_manager.current_theme
        
        self.setStyleSheet(f"""
            QListWidget {{
                background-color: {theme['backgrounds']['input']};
                color: {theme['text']['primary']};
                border: 1px solid {theme['borders']['inactive']};
                border-radius: 4px;
            }}
            QListWidget::item {{
                padding: 5px;
            }}
            QListWidget::item:selected {{
                background-color: {theme['accents']['primary']};
                color: {theme['text']['primary']};
            }}
            QListWidget::item:hover {{
                background-color: {theme['backgrounds']['secondary']};
            }}
        """)


class ThemedMenu(QMenu):
    """Themed menu"""
    
    def __init__(self, title="", parent=None):
        super().__init__(title, parent)
        self._theme_manager = ThemeManager()
        self._theme_manager.theme_changed.connect(self.apply_theme)
        self.apply_theme()
    
    def apply_theme(self):
        if not self._theme_manager.current_theme:
            return
        
        theme = self._theme_manager.current_theme
        
        self.setStyleSheet(f"""
            QMenu {{
                background-color: {theme['backgrounds']['secondary']};
                color: {theme['text']['primary']};
                border: 1px solid {theme['borders']['inactive']};
            }}
            QMenu::item {{
                padding: 5px 20px;
            }}
            QMenu::item:selected {{
                background-color: {theme['accents']['primary']};
            }}
        """)
