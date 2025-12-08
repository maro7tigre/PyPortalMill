# PyPortalMill: Project Planning & Brainstorming

## 1. Project Overview
**Goal**: Build a robust, highly customizable CNC generation tool capable of handling both Frames and Doors (and potentially other setups). The core philosophy is "Configuration over Code" — allowing users to define machine profiles, hardware types, and UI layouts without altering the source code.

## 2. Core Architecture
- **Language**: Python
- **GUI Framework**: PySide6 (Qt)

### 2.1. Design Pattern: MVVM-C (Model-View-ViewModel-Coordinator)
To handle the complexity of dynamic widgets, cross-parameter dependencies ("Auto" logic), and context switching, we will use **MVVM-C**.

#### Why MVVM-C?
- **Model**: definitive source of truth (JSON serializable configs).
- **View (Qt Widgets)**: Dumb components. They just display what the ViewModel tells them and emit signals on user interaction.
- **ViewModel (The Brains)**:
    - Holds the *state* of the UI (e.g., `is_read_only` when "Auto" is checked).
    - Handles **Validation**: Checks input before updating the Model.
    - Handles **Auto-Calculation**: Listens to changes in dependencies and updates itself.
- **Coordinator**:
    - Manages the **Application Flow**.
    - Handles creation and switching of Setup Tabs (Contexts).
    - Ensures the correct "Drawing Preview" is connected to the active "Setup Tab".

#### The Logic Flow
1.  **User** toggles "Auto" on `Parameter A`.
2.  **View** emits signal.
3.  **ViewModel** captures signal:
    - Sets `Parameter A` model state to `auto=True`.
    - Triggers `update_state()` -> Sets `is_read_only=True`.
    - Signals **View** to disable the input box.
    - Subscribes to `Parameter B` (the dependency) updates.
4.  **Coordinator** ensures this change propagates to the generic "Save" command if needed.

## 3. Key Features

### 3.1. Theme & UI Customization
- **Theme Engine**:
    - Support for modern, premium aesthetics (Dark Mode, Glassmorphism).
    - Loadable JSON/CSS themes to change color palettes (Accent, Background, Text) dynamically.
- **Widget Manager**:
    - A dedicated "Window Manager" or "Widget Layout" editor.
    - Allows users to configure which widgets are visible and where they dock.

### 3.2. Configuration & Profiles (The "Backbone")
- **Profile Definition**:
    - Defines the *capabilities* of the machine or the process.
    - **Hardware Types**:
        - Default: Hinges, Locks.
        - Custom: Users can add new types (e.g., Strike Plates, Closers, Electric Releases).
        - **Constraints**: Mark hardware types as `Required` (must present in UI) or `Optional`.
- **Import/Export**:
    - All configurations (profiles, setups, themes) must be serializable (JSON/YAML).
    - Ability to export a single "Setup" file to share between machines/users.

## 4. The Setup Editor (Advanced Logic)
This is the heart of the customization. It allows creating "Product Definitions" (e.g., "Standard Exterior Frame").

### 4.1. Multi-Tab Structure
- Users can create multiple **Setup Tabs**.
- Each tab represents a distinct production scenario.
- **Active Context**: Only the currently selected tab drives the Drawing Preview and Parameter list.
- **Switching**: Tabs on the right/top allow quick context switching between different setups.

### 4.2. Layout Logic (Left vs. Right)
- The UI layout for parameters is configurable per Setup.
- **Columns**: Control `Left Column` and `Right Column` count/distribution.
- **Categories**:
    - Users define Categories (e.g., "Dimensions", "Hardware Specs", "Finishing").
    - Assign Categories to Left or Right columns.

### 4.3. Parameter Definition
Each parameter within a category has deep configuration:
- **Attributes**: Name, Data Type (Float, Int, String, Enums), Default Value.
- **Auto & Active Logic**:
    - **Active Checkbox**: Toggle to enable/disable the parameter (is it used in calculation?).
    - **Auto Checkbox**: A flag that might trigger automatic calculation or default behavior.
- **Standalone Auto**:
    - A special "Master Auto" checkbox that exists outside standard parameters.
    - **Function**: Tying this master checkbox to multiple sub-parameters. When checked, it overrides or sets multiple fields to "Auto".

### 4.4. Special Categories
- **Image Preview**: A constrained category for static reference images (e.g., profile cross-section).
    - Position is configurable, but internal content is fixed (just the image).
- **Component Order**: A list view defining the machining order of operations.
    - Unique category: Can only set presence/position, not internal structure.

## 5. Parametric Drawing System
- **Dynamic Preview**: A canvas that renders the setup in real-time.
- **Binding System**:
    - **Variables**: The Drawing is not hardcoded. It uses variables (e.g., `$HEIGHT`, `$WIDTH`, `$LOCK_Y`).
    - **Linkage**: The Setup Editor includes a mapping interface:
        - `Drawing Dimension A` <-> `Parameter: Frame_Height`.
        - Positions can be fixed or variable.
    - **Tab Independence**: Each Setup Tab has its own drawing definition (or references a generic template with specific variable overrides).
- **Visualization**:
    - Only the drawing for the *opened* tab is active/visible.
