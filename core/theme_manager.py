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
        styles = theme.get('control_styles', {})
        
        # Helper for safer lookups
        def get_color(path, default="#000000"):
            parts = path.split('.')
            val = theme
            for p in parts:
                if isinstance(val, dict): val = val.get(p, {})
                else: return default
            return val if isinstance(val, str) else default

        def get_style(widget_type, prop, default):
            return styles.get(widget_type, {}).get(prop, default)

        # --- Base Colors ---
        bg_primary = get_color('backgrounds.primary', '#1d1f28')
        bg_secondary = get_color('backgrounds.secondary', '#0d0f18')
        bg_tertiary = get_color('backgrounds.tertiary', '#44475c')
        bg_input = get_color('backgrounds.input', '#1d1f28')
        
        text_primary = get_color('text.primary', '#ffffff')
        text_secondary = get_color('text.secondary', '#bdbdc0')
        
        border_active = get_color('borders.active', '#BB86FC')
        border_inactive = get_color('borders.inactive', '#6f779a')
        accent_primary = get_color('accents.primary', '#BB86FC')
        
        # --- Buttons ---
        btn_radius = get_style('buttons', 'border_radius', 4)
        btn_pad_h = get_style('buttons', 'padding_horizontal', 12)
        btn_pad_v = get_style('buttons', 'padding_vertical', 6)
        btn_font = get_style('buttons', 'font_size', 10)
        btn_border = get_style('buttons', 'border_width', 1)

        button_css = ""
        # Loop through all button types defined in theme['buttons']
        # e.g., neutral, primary, success, danger
        if 'buttons' in theme:
            for btn_type, states in theme['buttons'].items():
                # Base selector (e.g., QPushButton[class="primary"])
                # For 'neutral', we also apply it to the base QPushButton as default
                selector = f'QPushButton[class="{btn_type}"]'
                if btn_type == 'neutral': # Only neutral applies to default QPushButton
                     selector += ", QPushButton"
                
                # Normal State
                norm = states.get('normal', {})
                button_css += f"""
                {selector} {{
                    background-color: {norm.get('background', bg_tertiary)};
                    color: {norm.get('text', text_primary)};
                    border: {btn_border}px solid {norm.get('outline', border_inactive)};
                    border-radius: {btn_radius}px;
                    padding: {btn_pad_v}px {btn_pad_h}px;
                    font-size: {btn_font}pt;
                }}
                """
                
                # Hover State
                hov = states.get('hovered', {})
                button_css += f"""
                {selector}:hover {{
                    background-color: {hov.get('background', norm.get('background'))};
                    color: {hov.get('text', norm.get('text'))};
                    border: {btn_border}px solid {hov.get('outline', norm.get('outline'))};
                }}
                """
                
                # Pressed State
                prs = states.get('clicked', {}) # 'clicked' naming in json, 'pressed' in css
                button_css += f"""
                {selector}:pressed {{
                    background-color: {prs.get('background', norm.get('background'))};
                    color: {prs.get('text', norm.get('text'))};
                    border: {btn_border}px solid {prs.get('outline', norm.get('outline'))};
                }}
                """
                
                # Disabled State
                dis = states.get('disabled', {})
                button_css += f"""
                {selector}:disabled {{
                    background-color: {dis.get('background', bg_primary)};
                    color: {dis.get('text', text_secondary)};
                    border: {btn_border}px solid {dis.get('outline', border_inactive)};
                }}
                """

        # --- Inputs ---
        # Note: We prioritize the new dictionary-based config if it exists.
        # Legacy values are only used as defaults if strict lookup fails in the fallback block
        
        in_radius = 4
        in_pad_h = 8
        in_pad_v = 4
        in_font = 10
        in_border_w = 1
        in_focus_w = 2

        # Try to get control_styles if available for base geometry
        if 'control_styles' in theme and 'inputs' in theme['control_styles']:
             c_in = theme['control_styles']['inputs']
             in_radius = c_in.get('border_radius', 4)
             in_pad_h = c_in.get('padding_horizontal', 8)
             in_pad_v = c_in.get('padding_vertical', 4)
             in_font = c_in.get('font_size', 10)
             in_border_w = c_in.get('border_width', 1)
             in_focus_w = c_in.get('focus_border_width', 2)
        
        accent_error = get_color('accents.error', '#ff4a7c')
        
        input_css = ""
        # Check for new inputs configuration
        if 'inputs' in theme and isinstance(theme['inputs'], dict) and 'normal' in theme['inputs']:
            inp = theme['inputs']
            norm = inp.get('normal', {})
            foc = inp.get('focused', {})
            err = inp.get('error', {})
            dis = inp.get('disabled', {})
            
            # Base Input Style
            input_css += f"""
            QLineEdit, QSpinBox, QDoubleSpinBox, QTextEdit {{
                background-color: {norm.get('background', bg_input)};
                color: {norm.get('text', text_primary)};
                border: {in_border_w}px solid {norm.get('border', border_inactive)};
                border-radius: {in_radius}px;
                padding: {in_pad_v}px {in_pad_h}px;
                font-size: {in_font}pt;
            }}
            
            QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus, QTextEdit:focus {{
                background-color: {foc.get('background', bg_input)};
                color: {foc.get('text', text_primary)};
                border: {in_focus_w}px solid {foc.get('border', border_active)};
            }}
            
            QLineEdit[error="true"], QSpinBox[error="true"], QDoubleSpinBox[error="true"] {{
                background-color: {err.get('background', bg_input)};
                color: {err.get('text', text_primary)};
                border: {in_border_w}px solid {err.get('border', accent_error)};
            }}
            
            QLineEdit:disabled, QSpinBox:disabled, QDoubleSpinBox:disabled, QTextEdit:disabled {{
                background-color: {dis.get('background', bg_input)};
                color: {dis.get('text', text_secondary)};
                border: {in_border_w}px solid {dis.get('border', border_inactive)};
            }}
            """
        else:
            # Fallback to legacy styling
            input_css += f"""
            QLineEdit, QSpinBox, QDoubleSpinBox, QTextEdit {{
                background-color: {bg_input};
                color: {text_primary};
                border: {in_border_w}px solid {border_inactive};
                border-radius: {in_radius}px;
                padding: {in_pad_v}px {in_pad_h}px;
                font-size: {in_font}pt;
            }}
            
            QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus, QTextEdit:focus {{
                border: {in_focus_w}px solid {border_active};
                background-color: {bg_input};
            }}
            
            QLineEdit[error="true"], QSpinBox[error="true"], QDoubleSpinBox[error="true"] {{
                border: {in_border_w}px solid {accent_error};
            }}
            """

        # --- Layouts ---
        layouts = theme.get('layouts', {})
        p_grid = layouts.get('profile_grid', {})
        t_sel = layouts.get('type_selector', {})
        
        layout_css = f"""
        ProfileGrid, QWidget#ProfileGridContainer {{
            background-color: {p_grid.get('background', '#282a36')};
            border: 1px solid {p_grid.get('border', '#44475c')};
            border-radius: 4px;
        }}
        
        TypeSelector, QWidget#TypeSelectorContainer {{
             background-color: {t_sel.get('background', '#1d1f28')};
        }}
        """

        # --- Global Stylesheet ---
        stylesheet = f"""
        /* Global Reset */
        QMainWindow, QDialog, QWidget {{
            background-color: {bg_primary};
            color: {text_primary};
        }}
        
        /* Typography Helper (if needed) */
        QLabel {{ background: transparent; }}
        
        /* Links */
        QLabel[class="link"] {{
            color: {get_color('text.links', '#00c4fe')};
            text-decoration: underline;
        }}
        QLabel[class="link"]:hover {{
            color: {accent_primary};
        }}

        /* Buttons */
        {button_css}
        
        /* Inputs */
        {input_css}

        /* Layouts */
        {layout_css}
        
        /* Tabs */
        QTabWidget::pane {{
            border: 1px solid {border_inactive};
            background-color: {bg_secondary};
            border-radius: {btn_radius}px;
        }}
        QTabBar::tab {{
            background-color: {bg_tertiary};
            color: {text_secondary};
            padding: 6px 16px;
            border-top-left-radius: {btn_radius}px;
            border-top-right-radius: {btn_radius}px;
            margin-right: 2px;
        }}
        QTabBar::tab:selected {{
            background-color: {bg_secondary};
            color: {text_primary};
            border-bottom: 2px solid {accent_primary};
        }}
        
        /* Scrollbars */
        QScrollBar:vertical {{
            background-color: {bg_tertiary};
            width: 10px;
            margin: 0px;
        }}
        QScrollBar::handle:vertical {{
            background-color: {border_inactive};
            min-height: 20px;
            border-radius: 5px;
        }}
        QScrollBar::handle:vertical:hover {{
            background-color: {border_active};
        }}
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            height: 0px;
        }}
        
        /* Menus */
        QMenuBar {{ background-color: {bg_tertiary}; }}
        QMenuBar::item:selected {{ background-color: {bg_secondary}; }}
        QMenu {{ 
            background-color: {bg_secondary}; 
            border: 1px solid {border_inactive};
        }}
        QMenu::item:selected {{ background-color: {accent_primary}; }}
        
        /* Lists */
        QListWidget {{
            background-color: {bg_input};
            border: 1px solid {border_inactive};
            border-radius: {in_radius}px;
        }}
        QListWidget::item:selected {{
            background-color: {bg_tertiary}; 
            border: 1px solid {border_active};
            color: {text_primary};
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
