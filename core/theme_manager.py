"""
Theme Manager for PyPortalMill
Singleton class that handles theme loading, switching, and stylesheet generation
"""

import json
import os
from pathlib import Path
from typing import Dict, Optional, List
from PySide6.QtCore import QObject, Signal


class ThemeManager(QObject):
    """Manages application themes and provides stylesheet generation"""
    
    # Singleton instance
    _instance: Optional['ThemeManager'] = None
    
    # Signal emitted when theme changes
    theme_changed = Signal(str)  # theme_name
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        # Prevent re-initialization
        if hasattr(self, '_initialized'):
            return
        
        super().__init__()
        self._initialized = True
        
        # Paths
        self.themes_dir = Path(__file__).parent.parent / 'themes'
        self.user_themes_dir = self.themes_dir / 'user_themes'
        self.user_themes_dir.mkdir(exist_ok=True)
        
        # Data storage
        self.default_themes: Dict[str, Dict] = {}
        self.user_themes: Dict[str, Dict] = {}
        self.current_theme: Optional[Dict] = None
        self.current_theme_name: str = ""
        
        # Load themes
        self._load_default_themes()
        self._load_user_themes()
    
    def _load_default_themes(self):
        """Load default themes (purple, dark, light)"""
        default_theme_files = ['purple.json', 'dark.json', 'light.json']
        
        for filename in default_theme_files:
            theme_path = self.themes_dir / filename
            if theme_path.exists():
                with open(theme_path, 'r') as f:
                    theme_data = json.load(f)
                    theme_name = theme_data.get('name', filename.replace('.json', ''))
                    self.default_themes[theme_name] = theme_data
    
    def _load_user_themes(self):
        """Load user-created themes from user_themes directory"""
        self.user_themes = {}
        
        if not self.user_themes_dir.exists():
            return
        
        for theme_file in self.user_themes_dir.glob('*.json'):
            try:
                with open(theme_file, 'r') as f:
                    theme_data = json.load(f)
                    theme_name = theme_data.get('name', theme_file.stem)
                    self.user_themes[theme_name] = theme_data
            except Exception as e:
                print(f"Error loading user theme {theme_file}: {e}")
    
    def get_all_themes(self) -> List[str]:
        """Get list of all available theme names"""
        return list(self.default_themes.keys()) + list(self.user_themes.keys())
    
    def get_default_theme_names(self) -> List[str]:
        """Get list of default theme names"""
        return list(self.default_themes.keys())
    
    def get_user_theme_names(self) -> List[str]:
        """Get list of user theme names"""
        return list(self.user_themes.keys())
    
    def get_theme(self, theme_name: str) -> Optional[Dict]:
        """Get theme data by name"""
        if theme_name in self.default_themes:
            return self.default_themes[theme_name]
        elif theme_name in self.user_themes:
            return self.user_themes[theme_name]
        return None
    
    def set_theme(self, theme_name: str) -> bool:
        """Set the current active theme"""
        theme = self.get_theme(theme_name)
        if theme:
            self.current_theme = theme
            self.current_theme_name = theme_name
            self.theme_changed.emit(theme_name)
            return True
        return False
    
    def save_user_theme(self, theme_name: str, theme_data: Dict) -> bool:
        """Save a user theme to disk"""
        try:
            # Ensure name is in the theme data
            theme_data['name'] = theme_name
            
            # Save to file
            theme_file = self.user_themes_dir / f"{theme_name.lower().replace(' ', '_')}.json"
            with open(theme_file, 'w') as f:
                json.dump(theme_data, f, indent=2)
            
            # Update internal storage
            self.user_themes[theme_name] = theme_data
            
            return True
        except Exception as e:
            print(f"Error saving user theme {theme_name}: {e}")
            return False
    
    def delete_user_theme(self, theme_name: str) -> bool:
        """Delete a user theme"""
        try:
            if theme_name not in self.user_themes:
                return False
            
            # Delete from disk
            theme_file = self.user_themes_dir / f"{theme_name.lower().replace(' ', '_')}.json"
            if theme_file.exists():
                theme_file.unlink()
            
            # Remove from internal storage
            del self.user_themes[theme_name]
            
            return True
        except Exception as e:
            print(f"Error deleting user theme {theme_name}: {e}")
            return False
    
    def get_stylesheet(self) -> str:
        """Generate Qt stylesheet based on current theme"""
        if not self.current_theme:
            return ""
        
        theme = self.current_theme
        styles = theme.get('control_styles', {})  # Get control styles from theme
        
        # Extract colors
        bg_primary = theme['backgrounds']['primary']
        bg_secondary = theme['backgrounds']['secondary']
        bg_tertiary = theme['backgrounds']['tertiary']
        bg_input = theme['backgrounds']['input']
        
        text_primary = theme['text']['primary']
        text_secondary = theme['text']['secondary']
        text_disabled = theme['text']['disabled']
        
        accent_primary = theme['accents']['primary']
        border_active = theme['borders']['active']
        border_inactive = theme['borders']['inactive']
        
        # Extract style values
        btn_radius = styles.get('buttons', {}).get('border_radius', 4)
        btn_pad_h = styles.get('buttons', {}).get('padding_horizontal', 12)
        btn_pad_v = styles.get('buttons', {}).get('padding_vertical', 6)
        
        # Generate button styles
        button_styles = ""
        
        # Default button style (using 'primary' as default)
        default_btn_type = 'primary'
        if default_btn_type in theme['buttons']:
            colors = theme['buttons'][default_btn_type]
            button_styles += f"""
            QPushButton {{
                background-color: {colors['normal']['background']};
                color: {colors['normal']['text']};
                border: 2px solid {colors['normal']['outline']};
                border-radius: {btn_radius}px;
                padding: {btn_pad_v}px {btn_pad_h}px;
                font-size: {styles.get('buttons', {}).get('font_size', 10)}pt;
            }}
            
            QPushButton:hover {{
                background-color: {colors['hovered']['background']};
                color: {colors['hovered']['text']};
                border: 2px solid {colors['hovered']['outline']};
            }}
            
            QPushButton:pressed {{
                background-color: {colors['clicked']['background']};
                color: {colors['clicked']['text']};
                border: 2px solid {colors['clicked']['outline']};
            }}
            
            QPushButton:disabled {{
                background-color: {colors['disabled']['background']};
                color: {colors['disabled']['text']};
                border: 2px solid {colors['disabled']['outline']};
            }}
            """

        # Generate specific styles for all button types (primary, secondary, danger, etc.)
        for btn_type, colors in theme['buttons'].items():
            button_styles += f"""
            QPushButton[class="{btn_type}"] {{
                background-color: {colors['normal']['background']};
                color: {colors['normal']['text']};
                border: 2px solid {colors['normal']['outline']};
            }}
            
            QPushButton[class="{btn_type}"]:hover {{
                background-color: {colors['hovered']['background']};
                color: {colors['hovered']['text']};
                border: 2px solid {colors['hovered']['outline']};
            }}
            
            QPushButton[class="{btn_type}"]:pressed {{
                background-color: {colors['clicked']['background']};
                color: {colors['clicked']['text']};
                border: 2px solid {colors['clicked']['outline']};
            }}
            
            QPushButton[class="{btn_type}"]:disabled {{
                background-color: {colors['disabled']['background']};
                color: {colors['disabled']['text']};
                border: 2px solid {colors['disabled']['outline']};
            }}
            """
        
        # Build stylesheet
        stylesheet = f"""
        QMainWindow {{
            background-color: {bg_primary};
            color: {text_primary};
        }}
        
        QWidget {{
            background-color: {bg_primary};
            color: {text_primary};
        }}
        
        QTabWidget::pane {{
            border: 1px solid {border_inactive};
            background-color: {bg_secondary};
        }}
        
        QTabBar::tab {{
            background-color: {bg_tertiary};
            color: {text_secondary};
            padding: 8px 16px;
            border: 1px solid {border_inactive};
            border-bottom: none;
            border-top-left-radius: {btn_radius}px;
            border-top-right-radius: {btn_radius}px;
        }}
        
        QTabBar::tab:selected {{
            background-color: {bg_secondary};
            color: {text_primary};
            border-color: {border_active};
        }}
        
        QTabBar::tab:hover {{
            background-color: {bg_secondary};
        }}
        
        {button_styles}
        
        QLineEdit, QSpinBox, QDoubleSpinBox {{
            background-color: {bg_input};
            color: {text_primary};
            border: 1px solid {border_inactive};
            border-radius: {styles.get('inputs', {}).get('border_radius', 4)}px;
            padding: {styles.get('inputs', {}).get('padding_vertical', 4)}px {styles.get('inputs', {}).get('padding_horizontal', 8)}px;
        }}
        
        QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus {{
            border: {styles.get('inputs', {}).get('focus_border_width', 2)}px solid {border_active};
        }}
        
        QLabel {{
            color: {text_primary};
            background: transparent;
        }}
        
        QMenuBar {{
            background-color: {bg_tertiary};
            color: {text_primary};
        }}
        
        QMenuBar::item:selected {{
            background-color: {bg_secondary};
        }}
        
        QMenu {{
            background-color: {bg_secondary};
            color: {text_primary};
            border: 1px solid {border_inactive};
        }}
        
        QMenu::item:selected {{
            background-color: {accent_primary};
        }}
        
        QDialog {{
            background-color: {bg_primary};
            color: {text_primary};
        }}
        
        QListWidget {{
            background-color: {bg_input};
            color: {text_primary};
            border: 1px solid {border_inactive};
        }}
        
        QListWidget::item:selected {{
            background-color: {accent_primary};
        }}
        
        QScrollBar:vertical {{
            background-color: {bg_tertiary};
            width: 12px;
        }}
        
        QScrollBar::handle:vertical {{
            background-color: {border_inactive};
            border-radius: 6px;
        }}
        
        QScrollBar::handle:vertical:hover {{
            background-color: {border_active};
        }}
        """
        
        return stylesheet
    
    def get_color(self, path: str) -> str:
        """Get a color value from current theme by path (e.g., 'backgrounds.primary')"""
        if not self.current_theme:
            return "#000000"
        
        parts = path.split('.')
        value = self.current_theme
        
        for part in parts:
            if isinstance(value, dict) and part in value:
                value = value[part]
            else:
                return "#000000"
        
        return value
    
    def get_style(self, path: str):
        """Get a style value from current theme's control styles by path (e.g., 'buttons.border_radius')"""
        if not self.current_theme or 'control_styles' not in self.current_theme:
            return None
        
        parts = path.split('.')
        value = self.current_theme['control_styles']
        
        for part in parts:
            if isinstance(value, dict) and part in value:
                value = value[part]
            else:
                return None
        
        return value


# Convenience function to get the singleton instance
def get_theme_manager() -> ThemeManager:
    """Get the ThemeManager singleton instance"""
    return ThemeManager()
