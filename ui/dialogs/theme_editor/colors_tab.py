"""
Colors Tab for Theme Editor
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QScrollArea,
                               QGroupBox, QLabel, QPushButton, QColorDialog,
                               QGridLayout, QFrame)
from PySide6.QtGui import QColor
from PySide6.QtCore import Qt


class ColorsTab(QWidget):
    """Colors tab for theme customization"""
    
    def __init__(self, parent_dialog):
        super().__init__()
        self.parent_dialog = parent_dialog
        self.color_buttons = {}  # Store references to color picker buttons
        self.preview_widgets = {}  # Store references to preview widgets
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup the UI"""
        layout = QVBoxLayout(self)
        
        # Scrollable area for all sections
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        
        # Create sections
        self._create_background_section(scroll_layout)
        self._create_text_section(scroll_layout)
        self._create_accent_section(scroll_layout)
        self._create_border_section(scroll_layout)
        self._create_button_states_section(scroll_layout)
        
        scroll_layout.addStretch()
        scroll.setWidget(scroll_widget)
        layout.addWidget(scroll)
    
    def _create_background_section(self, parent_layout):
        """Create background colors section"""
        group = QGroupBox("Background Colors")
        main_layout = QHBoxLayout()
        
        # Color controls on left
        controls_layout = QGridLayout()
        row = 0
        
        for key, label in [('primary', 'Primary'), ('secondary', 'Secondary'),
                          ('tertiary', 'Tertiary'), ('input', 'Input Fields')]:
            controls_layout.addWidget(QLabel(label + ":"), row, 0)
            color_btn = self._create_color_button(f'backgrounds.{key}')
            controls_layout.addWidget(color_btn, row, 1)
            row += 1
        
        controls_layout.setRowStretch(row, 1)  # Add stretch after controls
        main_layout.addLayout(controls_layout)
        main_layout.addStretch(1)  # Add stretch between controls and preview
        
        # Preview on right
        preview = QLabel("Background Preview")
        preview.setFixedSize(150, 100)
        preview.setStyleSheet(f"background-color: {self._get_color('backgrounds.primary')}; color: {self._get_color('text.primary')}; border: 1px solid {self._get_color('borders.inactive')}; padding: 10px;")
        self.preview_widgets['background'] = preview
        main_layout.addWidget(preview)
        
        group.setLayout(main_layout)
        parent_layout.addWidget(group)
    
    def _create_text_section(self, parent_layout):
        """Create text colors section"""
        group = QGroupBox("Text Colors")
        main_layout = QHBoxLayout()
        
        # Color controls on left
        controls_layout = QGridLayout()
        row = 0
        
        for key, label in [('primary', 'Primary'), ('secondary', 'Secondary'),
                          ('disabled', 'Disabled'), ('links', 'Links/Highlights')]:
            controls_layout.addWidget(QLabel(label + ":"), row, 0)
            color_btn = self._create_color_button(f'text.{key}')
            controls_layout.addWidget(color_btn, row, 1)
            row += 1
        
        controls_layout.setRowStretch(row, 1)  # Add stretch after controls
        main_layout.addLayout(controls_layout)
        main_layout.addStretch(1)  # Add stretch between controls and preview
        
        # Preview on right
        preview_layout = QVBoxLayout()
        text_previews = []
        text_previews.append(self._create_text_label("Primary Text", 'text.primary'))
        text_previews.append(self._create_text_label("Secondary Text", 'text.secondary'))
        text_previews.append(self._create_text_label("Disabled Text", 'text.disabled'))
        text_previews.append(self._create_text_label("Link Text", 'text.links'))
        for label in text_previews:
            preview_layout.addWidget(label)
        self.preview_widgets['text_labels'] = text_previews
        preview_layout.addStretch()
        main_layout.addLayout(preview_layout)
        
        group.setLayout(main_layout)
        parent_layout.addWidget(group)
    
    def _create_accent_section(self, parent_layout):
        """Create accent colors section"""
        group = QGroupBox("Accent Colors")
        main_layout = QHBoxLayout()
        
        # Color controls on left
        controls_layout = QGridLayout()
        row = 0
        
        for key, label in [('primary', 'Primary'), ('secondary', 'Success'),
                          ('warning', 'Warning'), ('error', 'Error')]:
            controls_layout.addWidget(QLabel(label + ":"), row, 0)
            color_btn = self._create_color_button(f'accents.{key}')
            controls_layout.addWidget(color_btn, row, 1)
            row += 1
        
        controls_layout.setRowStretch(row, 1)  # Add stretch after controls
        main_layout.addLayout(controls_layout)
        main_layout.addStretch(1)  # Add stretch between controls and preview
        
        # Preview on right
        preview_layout = QGridLayout()
        accent_boxes = []
        accent_boxes.append(self._create_accent_box("Primary", 'accents.primary'))
        accent_boxes.append(self._create_accent_box("Success", 'accents.secondary'))
        accent_boxes.append(self._create_accent_box("Warning", 'accents.warning'))
        accent_boxes.append(self._create_accent_box("Error", 'accents.error'))
        preview_layout.addWidget(accent_boxes[0], 0, 0)
        preview_layout.addWidget(accent_boxes[1], 0, 1)
        preview_layout.addWidget(accent_boxes[2], 1, 0)
        preview_layout.addWidget(accent_boxes[3], 1, 1)
        self.preview_widgets['accent_boxes'] = accent_boxes
        preview_layout.setRowStretch(2, 1)  # Add stretch after preview
        main_layout.addLayout(preview_layout)
        
        group.setLayout(main_layout)
        parent_layout.addWidget(group)
    
    def _create_border_section(self, parent_layout):
        """Create border colors section"""
        group = QGroupBox("Border Colors")
        main_layout = QHBoxLayout()
        
        # Color controls on left
        controls_layout = QGridLayout()
        row = 0
        
        for key, label in [('active', 'Active'), ('inactive', 'Inactive')]:
            controls_layout.addWidget(QLabel(label + ":"), row, 0)
            color_btn = self._create_color_button(f'borders.{key}')
            controls_layout.addWidget(color_btn, row, 1)
            row += 1
        
        controls_layout.setRowStretch(row, 1)  # Add stretch after controls
        main_layout.addLayout(controls_layout)
        main_layout.addStretch(1)  # Add stretch between controls and preview
        
        # Preview on right
        preview_layout = QVBoxLayout()
        active_box = QFrame()
        active_box.setFixedSize(100, 40)
        active_box.setStyleSheet(f"border: 2px solid {self._get_color('borders.active')}; background: transparent;")
        inactive_box = QFrame()
        inactive_box.setFixedSize(100, 40)
        inactive_box.setStyleSheet(f"border: 2px solid {self._get_color('borders.inactive')}; background: transparent;")
        self.preview_widgets['border_active'] = active_box
        self.preview_widgets['border_inactive'] = inactive_box
        preview_layout.addWidget(QLabel("Active:"))
        preview_layout.addWidget(active_box)
        preview_layout.addWidget(QLabel("Inactive:"))
        preview_layout.addWidget(inactive_box)
        preview_layout.addStretch()
        main_layout.addLayout(preview_layout)
        
        group.setLayout(main_layout)
        parent_layout.addWidget(group)
    
    def _create_button_states_section(self, parent_layout):
        """Create button states section with all button types"""
        group = QGroupBox("Button States")
        layout = QVBoxLayout()
        
        button_types = [
            ('danger', 'Danger Button (Cancel/Close)'),
            ('success', 'Success Button (Confirm/Next)'),
            ('neutral', 'Neutral Button'),
            ('primary', 'Primary Button'),
            ('secondary', 'Secondary Button'),
            ('tertiary', 'Tertiary Button')
        ]
        
        for btn_type, label in button_types:
            btn_group = self._create_button_type_section(btn_type, label)
            layout.addWidget(btn_group)
        
        group.setLayout(layout)
        parent_layout.addWidget(group)
    
    def _create_button_type_section(self, button_type, label):
        """Create section for a specific button type"""
        group = QGroupBox(label)
        main_layout = QHBoxLayout()
        
        # Color controls for each state on left
        states_layout = QGridLayout()
        states_layout.addWidget(QLabel("State"), 0, 0)
        states_layout.addWidget(QLabel("Background"), 0, 1)
        states_layout.addWidget(QLabel("Outline"), 0, 2)
        states_layout.addWidget(QLabel("Text"), 0, 3)
        
        row = 1
        for state in ['normal', 'hovered', 'clicked', 'disabled']:
            states_layout.addWidget(QLabel(state.capitalize()), row, 0)
            states_layout.addWidget(self._create_color_button(f'buttons.{button_type}.{state}.background'), row, 1)
            states_layout.addWidget(self._create_color_button(f'buttons.{button_type}.{state}.outline'), row, 2)
            states_layout.addWidget(self._create_color_button(f'buttons.{button_type}.{state}.text'), row, 3)
            row += 1
        
        states_layout.setRowStretch(row, 1)  # Add stretch after controls
        main_layout.addLayout(states_layout)
        main_layout.addStretch(1)  # Add stretch between controls and preview
        
        # Preview buttons on right (Normal and Disabled)
        preview_layout = QVBoxLayout()
        preview_layout.addWidget(QLabel("Preview:"))
        
        normal_btn = QPushButton("Normal State")
        self._apply_button_style(normal_btn, button_type, 'normal')
        preview_layout.addWidget(normal_btn)
        
        disabled_btn = QPushButton("Disabled State")
        self._apply_button_style(disabled_btn, button_type, 'disabled')
        disabled_btn.setEnabled(False)
        preview_layout.addWidget(disabled_btn)
        
        # Store preview buttons
        if 'button_previews' not in self.preview_widgets:
            self.preview_widgets['button_previews'] = {}
        self.preview_widgets['button_previews'][button_type] = {'normal': normal_btn, 'disabled': disabled_btn}
        
        preview_layout.addStretch()
        main_layout.addLayout(preview_layout)
        
        group.setLayout(main_layout)
        return group
    
    def _create_color_button(self, color_path):
        """Create a color picker button"""
        color = self._get_color(color_path)
        btn = QPushButton()
        btn.setFixedSize(60, 30)
        btn.setStyleSheet(f"background-color: {color}; border: 1px solid #666;")
        btn.clicked.connect(lambda: self._pick_color(color_path, btn))
        
        # Store reference
        self.color_buttons[color_path] = btn
        
        return btn
    
    def _create_text_label(self, text, color_path):
        """Create a text label with specified color"""
        label = QLabel(text)
        label.setStyleSheet(f"color: {self._get_color(color_path)}; background: transparent; font-size: 11pt;")
        return label
    
    def _create_accent_box(self, text, color_path):
        """Create an accent color preview box"""
        label = QLabel(text)
        label.setFixedSize(80, 40)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet(f"background-color: {self._get_color(color_path)}; color: white; border-radius: 4px;")
        return label
    
    def _get_color(self, path):
        """Get color from theme data"""
        theme_data = self.parent_dialog.get_theme_data()
        if not theme_data:
            return "#000000"
        
        parts = path.split('.')
        value = theme_data
        for part in parts:
            if isinstance(value, dict) and part in value:
                value = value[part]
            else:
                return "#000000"
        
        return value
    
    def _set_color(self, path, color):
        """Set color in theme data"""
        theme_data = self.parent_dialog.get_theme_data()
        
        parts = path.split('.')
        current = theme_data
        for i, part in enumerate(parts[:-1]):
            if part not in current:
                current[part] = {}
            current = current[part]
        
        current[parts[-1]] = color
    
    def _pick_color(self, color_path, button):
        """Open color picker dialog"""
        current_color = QColor(self._get_color(color_path))
        color = QColorDialog.getColor(current_color, self, "Pick Color")
        
        if color.isValid():
            color_hex = color.name()
            self._set_color(color_path, color_hex)
            button.setStyleSheet(f"background-color: {color_hex}; border: 1px solid #666;")
            self._update_previews()
    
    def _apply_button_style(self, button, button_type, state):
        """Apply style to a preview button with interactive states"""
        bg = self._get_color(f'buttons.{button_type}.{state}.background')
        outline = self._get_color(f'buttons.{button_type}.{state}.outline')
        text = self._get_color(f'buttons.{button_type}.{state}.text')
        
        # Get hover and pressed states
        bg_hover = self._get_color(f'buttons.{button_type}.hovered.background')
        outline_hover = self._get_color(f'buttons.{button_type}.hovered.outline')
        text_hover = self._get_color(f'buttons.{button_type}.hovered.text')
        
        bg_pressed = self._get_color(f'buttons.{button_type}.clicked.background')
        outline_pressed = self._get_color(f'buttons.{button_type}.clicked.outline')
        text_pressed = self._get_color(f'buttons.{button_type}.clicked.text')
        
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {bg};
                border: 2px solid {outline};
                color: {text};
                padding: 6px 12px;
                border-radius: 4px;
            }}
            QPushButton:hover {{
                background-color: {bg_hover};
                border: 2px solid {outline_hover};
                color: {text_hover};
            }}
            QPushButton:pressed {{
                background-color: {bg_pressed};
                border: 2px solid {outline_pressed};
                color: {text_pressed};
            }}
            QPushButton:disabled {{
                background-color: {bg};
                border: 2px solid {outline};
                color: {text};
            }}
        """)
    
    def _update_previews(self):
        """Update all preview elements and apply temporary theme"""
        # Update background preview
        if 'background' in self.preview_widgets:
            self.preview_widgets['background'].setStyleSheet(
                f"background-color: {self._get_color('backgrounds.primary')}; "
                f"color: {self._get_color('text.primary')}; "
                f"border: 1px solid {self._get_color('borders.inactive')}; "
                f"padding: 10px;"
            )
        
        # Update text labels
        if 'text_labels' in self.preview_widgets:
            colors = ['text.primary', 'text.secondary', 'text.disabled', 'text.links']
            for i, label in enumerate(self.preview_widgets['text_labels']):
                label.setStyleSheet(f"color: {self._get_color(colors[i])}; background: transparent; font-size: 11pt;")
        
        # Update accent boxes
        if 'accent_boxes' in self.preview_widgets:
            colors = ['accents.primary', 'accents.secondary', 'accents.warning', 'accents.error']
            for i, box in enumerate(self.preview_widgets['accent_boxes']):
                box.setStyleSheet(f"background-color: {self._get_color(colors[i])}; color: white; border-radius: 4px;")
        
        # Update border previews
        if 'border_active' in self.preview_widgets:
            self.preview_widgets['border_active'].setStyleSheet(
                f"border: 2px solid {self._get_color('borders.active')}; background: transparent;"
            )
        if 'border_inactive' in self.preview_widgets:
            self.preview_widgets['border_inactive'].setStyleSheet(
                f"border: 2px solid {self._get_color('borders.inactive')}; background: transparent;"
            )
        
        # Update button previews
        if 'button_previews' in self.preview_widgets:
            for button_type, buttons in self.preview_widgets['button_previews'].items():
                self._apply_button_style(buttons['normal'], button_type, 'normal')
                self._apply_button_style(buttons['disabled'], button_type, 'disabled')
        
        # Trigger real-time theme update for the app
        self.parent_dialog.apply_temporary_theme()
    
    def get_theme_data(self):
        """Get the current theme data"""
        return self.parent_dialog.get_theme_data()
