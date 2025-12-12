# PyPortalMill Theming System

This document explains how the theming system works in PyPortalMill, how to use different widget styles, and how to extend the theme with new widgets.

## Overview

The theming system is built around:
1.  **Theme Files**: JSON files in `themes/` (defaults) and `themes/user_themes/` that define colors and style parameters.
2.  **Theme Manager**: `core/theme_manager.py` which reads the active theme JSON and generates a Qt Stylesheet (CSS) that is applied to the entire application.

## Using Button Styles

The theme system supports multiple button styles (e.g., `primary`, `secondary`, `danger`, `success`).

### Default Style
By default, any `QPushButton` created in the app uses the `primary` style defined in the theme.

### Applying Specific Styles
To use a specific style (like "danger" for a delete button), use the `setProperty` method on the widget:

```python
# Create a button
delete_btn = QPushButton("Delete Item")

# Apply the "danger" style
delete_btn.setProperty("class", "danger")

# You can also use other types defined in your theme JSON:
# save_btn.setProperty("class", "success")
# cancel_btn.setProperty("class", "secondary")
```

Note: The value passed to "class" must match a key in the `buttons` section of your theme JSON file.

## Theme JSON Structure

A theme JSON file looks like this:

```json
{
    "name": "My Theme",
    "backgrounds": { ... },
    "text": { ... },
    "buttons": {
        "primary": {
            "normal": { "background": "...", "text": "...", "outline": "..." },
            "hovered": { ... },
            "clicked": { ... },
            "disabled": { ... }
        },
        "danger": {
            ...
        }
    },
    "control_styles": {
        "buttons": { "border_radius": 4, ... }
    }
}
```

## Adding New Widgets to the Theme

To add support for a new widget type (e.g., `QComboBox` or `QCheckBox`):

### 1. Update the Theme JSON
Add any necessary colors or specific styles to your theme JSON file. For example:

```json
"control_styles": {
    "combobox": {
        "padding": 5
    }
}
```

### 2. Update Theme Manager (`core/theme_manager.py`)
You must update the `get_stylesheet()` method in `core/theme_manager.py` to generate the CSS for your new widget.

1.  Open `core/theme_manager.py`.
2.  Inside `get_stylesheet`, extract your new values:
    ```python
    combo_padding = styles.get('combobox', {}).get('padding', 5)
    ```
3.  Add the CSS rule to the `stylesheet` f-string:
    ```python
    stylesheet = f"""
    ...
    QComboBox {{
        background-color: {bg_input};
        color: {text_primary};
        padding: {combo_padding}px;
        border: 1px solid {border_inactive};
    }}
    
    QComboBox::drop-down {{
        border: none;
    }}
    ...
    """
    ```

Once updated, restarting the application or switching themes will apply the new styles to all instances of that widget.

## Advanced: Custom Widgets with Direct Theme Access

For complex custom widgets that act as containers or require dynamic painting (like `CardItem`, `StatusCard`, or custom drawing widgets), relying solely on the global stylesheet might not be sufficient. In these cases, you can access the `ThemeManager` directly.

### Pattern for Direct Access

1.  **Inherit from `ThemedWidgetMixin`**: This ensures your widget listens to the `theme_changed` signal.
2.  **Override `on_theme_changed`**: Call your custom update method.
3.  **Use `get_theme_manager()`**: Fetch specific colors using dot notation matching your theme JSON structure.

### Example Implementation

```python
from PySide6.QtWidgets import QFrame, QVBoxLayout
from core.theme_manager import get_theme_manager
from widgets.mixins import ThemedWidgetMixin

class MyCustomWidget(QFrame, ThemedWidgetMixin):
    def __init__(self, parent=None):
        super().__init__(parent)
        ThemedWidgetMixin.__init__(self)  # Initialize mixin
        
        self.layout = QVBoxLayout(self)
        self.update_style()  # Initial style application

    def on_theme_changed(self, theme_name):
        """Signal handler called when theme switches"""
        self.update_style()

    def update_style(self):
        """Fetch colors and apply them"""
        tm = get_theme_manager()
        
        # safely fetch colors with fallbacks
        bg_color = tm.get_color("backgrounds.tertiary")
        border_color = tm.get_color("borders.active")
        
        # Apply specifically to this widget instance
        self.setStyleSheet(f"""
            MyCustomWidget {{
                background-color: {bg_color};
                border: 2px solid {border_color};
                border-radius: 8px;
            }}
        """)
```

This pattern allows for highly granular control, such as changing border colors based on state (e.g., success/error) or drawing custom graphics in `paintEvent` using theme colors.
