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
