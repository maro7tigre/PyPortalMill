# Configuration System Plan

This document outlines the architecture for the `PyPortalMill` configuration system. The system uses Python-based configuration files to define the application's structure, tabs, profiles, and parameter behaviors, allowing for dynamic logic (methods/lambdas) to be directly embedded in the config.

## 1. System Overview

The configuration system is central to the application, driving the UI generation and logic execution.
- **Format**: Python files (`.py`) exporting a configuration dictionary.
- **Location**: `config/` directory.
- **Flexibility**: Supports multiple configuration files (e.g., `door_system.py`, `window_system.py`). Users can switch between these "System Configurations" via the app menu.

---

## 2. Configuration Structure

Each configuration file exports a dictionary representing a **System**, which contains one or more **Tabs**. Each Tab acts as a self-contained wizard.

### 2.1 Main Branch (Tab Definition)

The root structure defines the list of Tabs.

```python
system_config = {
    "tabs": [
        {
            "id": "frame_tab",
            "display_name": {"en": "Frame", "es": "Marco", "fr": "Cadre"},
            "icon": "frame_icon.svg",
             # ... content defined below
        },
        # ... other tabs
    ]
}
```

### 2.2 Tab Internal Structure

Each Tab contains the following key components:

1.  **Profiles**: Selection wizards for hardware/types (e.g., Lock Type, Hinge Type).
2.  **Preset Sections**: specialized UI components (Previews, Ordering).
3.  **Sections**: Groups of configurable attributes (Dimensions, Offsets).
4.  **Layout**: Positional arrangement of sections (Left, Mid, Right columns).
5.  **Generated GCode**: Definitions for the final output.

---

## 3. Component Details

### 3.1 Profiles
Profiles are dropdowns or grid selections that set a specific value (e.g., the model string) and require user selection.

- **Schema**:
  ```python
  "profiles": {
      "Lock": {
          "display_name": {"en": "Lock", "es": "Cerradura"},
          "required": True,
          "parameter_name": "frame_selected_lock",
          "type": "profile_grid", # or "combobox"
      },
      "Hinges": {
          "display_name": {"en": "Hinges"},
          "required": True,
          "parameter_name": "frame_selected_hinge"
      }
  }
  ```

### 3.2 Preset Sections
These are "Special" sections with hardcoded logic for specific tasks, but configurable via parameters.

- **Parameter Preview**:
  - **Type**: `image_preview`
  - **Function**: Displays an image from a directory based on the value of a specific parameter.
  - **Config**: `directory`: Path to images. `parameter`: The parameter to watch (e.g., `frame_type`).
- **Component Order**:
  - **Type**: `execution_order`
  - **Function**: Reorderable list of active components.
  - **Logic**: derived from an `listings` method that returns valid components.
  - **Config**: `parameter`: variable to store the final list order.

### 3.3 Sections & Attributes
Sections classify attributes into logical groups (e.g., "Dimensions", "Hardware Defaults").

- **Standard Attribute** (`float`, `int`, `str`, `bool`)
  - Basic input fields via LineEdit, SpinBox, or CheckBox.
  - **Schema**:
    ```python
    "Frame Height": {
        "display_name": {"en": "Frame Height"},
        "type": "float",
        "default_value": 2100.0,
        "min": 500.0,
        "max": 3400.0,
        "parameter_name": "frame_height"
    }
    ```

- **Auto Attribute** (Composite Widget)
  - **UI**: [Checkbox "Auto"] + [Input Field].
  - **Logic**:
    - If `Auto` is Checked: Input is disabled. Value is derived from `calc` method.
    - If `Auto` is Unchecked: Input is enabled. User enters manually.
  - **Schema**:
    ```python
    "Y Offset": {
        "display_name": {"en": "Y Offset"},
        "type": "float",
        "auto": True,     # Enables the Auto checkbox
        "calc": lambda params: params['frame_height'] / 2, # Method to calculate value
        "active": False,  # Does not have 'Active' checkbox
        "parameter_name": "lock_y_offset"
    }
    ```

- **Active Attribute** (Composite Widget)
  - **UI**: [Checkbox "Active"] + [Input Field] (or just Checkbox if boolean).
  - **Logic**:
    - If `Active` is Checked: The attribute/component is included in the `Component Order` active list.
    - If `Active` is Unchecked: It is removed from the order and processing.
  - **Schema**:
    ```python
    "Lock Configuration": {
        "active": True, # Enables the Active checkbox
        # ...
    }
    ```

- **Multi-Attribute** (Dynamic Spawner)
  - **UI**: An `int` input (e.g., "Number of Hinges: 3").
  - **Logic**: Spawns `N` copies of a template attribute.
  - **Schema**:
    ```python
    "Hinges Count": {
        "type": "multi_attribute",
        "default": 3,
        "min": 0,
        "max": 5,
        "template": {
            "display_name": "Hinge # Position", # # is replaced by index
            "parameter_name": "hinge_#_pos",
            "type": "float",
            "auto": True,
            "calc": calculate_hinge_pos # Method handling index
        }
    }
    ```

- **Grouped Auto** (Section Level)
  - **UI**: A master "Auto" checkbox for the whole section.
  - **Logic**: Toggles `Auto` state for *all* children attributes defined in `attributes`.

---

### 3.4 Layout (Section Positions)
Defines where sections appear in the "Setup" sub-tab (Center Pane).

```python
"sections_positions": {
    "left": ["Frame Configurations", "Parameter Preview"],
    "mid": ["Component Order"], # "mid_tap" in user prompt
    "right": ["Generated GCode Status"]
}
```

### 3.5 Generated GCode
The final output definition, tracked in the last wizard step.

- **Schema**:
  ```python
  "generated_gcode": [
      {
          "label": "Lock GCode",
          "parameter": "selected_lock",
          "type": "gcode_status_card"
      },
      # ...
  ]
  ```

---

## 4. UI Implementation Strategy

### Widget Factory
A `WidgetFactory` will parse the `type` field of each attribute and return the appropriate Composite Widget.

- **ComplexLogicWidget**: Base class for widgets with `Auto`/`Active` flags.
  - Connects `toggled` signals of checkboxes to the parameter logic.
  - Connects `textChanged` or `valueChanged` to the parameter store.
  - Listens for `variable_updated` signals to re-run `calc` methods if in Auto mode.

### Tab Wizard Layout
Each Tab renders as a 3-step process (internally or via sub-tabs):
1.  **Selection/Profile**: Renders `Profiles`.
2.  **Configuration**: Renders `Sections` based on `sections_positions`.
3.  **Generation**: Renders `Generated GCode` list and progress.

### Method Handling
Since config is Python, `calc` and `listings` keys will hold direct references to Python functions or lambdas. The `ConfigManager` will simply evaluate these when required.
