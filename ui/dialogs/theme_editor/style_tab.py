"""
Style Tab for Theme Editor
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QScrollArea,
                               QGroupBox, QLabel, QSpinBox, QFormLayout, 
                               QPushButton, QLineEdit, QFrame, QAbstractSpinBox)
from PySide6.QtCore import Qt


class StyleTab(QWidget):
    """Style tab for theme customization"""
    
    def __init__(self, parent_dialog):
        super().__init__()
        self.parent_dialog = parent_dialog
        self.style_inputs = {}  # Store references to style input widgets
        self.preview_widgets = {}  # Store preview widgets
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup the UI"""
        layout = QVBoxLayout(self)
        
        # Scrollable area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        
        # Create sections with previews on the right
        self._create_button_styles_section(scroll_layout)
        self._create_input_styles_section(scroll_layout)
        self._create_card_styles_section(scroll_layout)
        self._create_label_styles_section(scroll_layout)
        
        scroll_layout.addStretch()
        scroll.setWidget(scroll_widget)
        layout.addWidget(scroll)
    
    def _create_button_styles_section(self, parent_layout):
        """Create button styles section with preview on right"""
        group = QGroupBox("Button Styles")
        main_layout = QHBoxLayout()
        
        # Controls on left
        controls_layout = QFormLayout()
        
        # Border radius
        radius_spin = QSpinBox()
        radius_spin.setRange(0, 50)
        radius_spin.setValue(self._get_style('buttons.border_radius', 4))
        radius_spin.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.PlusMinus)
        radius_spin.valueChanged.connect(lambda: self._update_button_preview())
        self.style_inputs['buttons.border_radius'] = radius_spin
        controls_layout.addRow("Border Radius (px):", radius_spin)
        
        # Padding horizontal
        pad_h_spin = QSpinBox()
        pad_h_spin.setRange(0, 50)
        pad_h_spin.setValue(self._get_style('buttons.padding_horizontal', 12))
        pad_h_spin.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.PlusMinus)
        pad_h_spin.valueChanged.connect(lambda: self._update_button_preview())
        self.style_inputs['buttons.padding_horizontal'] = pad_h_spin
        controls_layout.addRow("Padding Horizontal (px):", pad_h_spin)
        
        # Padding vertical
        pad_v_spin = QSpinBox()
        pad_v_spin.setRange(0, 50)
        pad_v_spin.setValue(self._get_style('buttons.padding_vertical', 6))
        pad_v_spin.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.PlusMinus)
        pad_v_spin.valueChanged.connect(lambda: self._update_button_preview())
        self.style_inputs['buttons.padding_vertical'] = pad_v_spin
        controls_layout.addRow("Padding Vertical (px):", pad_v_spin)
        
        # Font size
        font_spin = QSpinBox()
        font_spin.setRange(6, 24)
        font_spin.setValue(self._get_style('buttons.font_size', 10))
        font_spin.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.PlusMinus)
        font_spin.valueChanged.connect(lambda: self._update_button_preview())
        self.style_inputs['buttons.font_size'] = font_spin
        controls_layout.addRow("Font Size (pt):", font_spin)
        
        # Border width
        border_spin = QSpinBox()
        border_spin.setRange(0, 10)
        border_spin.setValue(self._get_style('buttons.border_width', 1))
        border_spin.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.PlusMinus)
        border_spin.valueChanged.connect(lambda: self._update_button_preview())
        self.style_inputs['buttons.border_width'] = border_spin
        controls_layout.addRow("Border Width (px):", border_spin)
        
        main_layout.addLayout(controls_layout)
        main_layout.addStretch(1)  # Add stretch between controls and preview
        
        # Preview on right
        preview_layout = QVBoxLayout()
        preview_layout.addWidget(QLabel("Preview:"))
        
        preview_button = QPushButton("Button Preview")
        preview_button.setFixedSize(150, 40)
        self.preview_widgets['button'] = preview_button
        preview_layout.addWidget(preview_button)
        preview_layout.addStretch()
        
        main_layout.addLayout(preview_layout)
        
        group.setLayout(main_layout)
        parent_layout.addWidget(group)
        
        # Initial update
        self._update_button_preview()
    
    def _create_input_styles_section(self, parent_layout):
        """Create input styles section with preview on right"""
        group = QGroupBox("Input Field Styles")
        main_layout = QHBoxLayout()
        
        # Controls on left
        controls_layout = QFormLayout()
        
        # Border radius
        radius_spin = QSpinBox()
        radius_spin.setRange(0, 50)
        radius_spin.setValue(self._get_style('inputs.border_radius', 4))
        radius_spin.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.PlusMinus)
        radius_spin.valueChanged.connect(lambda: self._update_input_preview())
        self.style_inputs['inputs.border_radius'] = radius_spin
        controls_layout.addRow("Border Radius (px):", radius_spin)
        
        # Padding horizontal
        pad_h_spin = QSpinBox()
        pad_h_spin.setRange(0, 50)
        pad_h_spin.setValue(self._get_style('inputs.padding_horizontal', 8))
        pad_h_spin.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.PlusMinus)
        pad_h_spin.valueChanged.connect(lambda: self._update_input_preview())
        self.style_inputs['inputs.padding_horizontal'] = pad_h_spin
        controls_layout.addRow("Padding Horizontal (px):", pad_h_spin)
        
        # Padding vertical
        pad_v_spin = QSpinBox()
        pad_v_spin.setRange(0, 50)
        pad_v_spin.setValue(self._get_style('inputs.padding_vertical', 4))
        pad_v_spin.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.PlusMinus)
        pad_v_spin.valueChanged.connect(lambda: self._update_input_preview())
        self.style_inputs['inputs.padding_vertical'] = pad_v_spin
        controls_layout.addRow("Padding Vertical (px):", pad_v_spin)
        
        # Font size
        font_spin = QSpinBox()
        font_spin.setRange(6, 24)
        font_spin.setValue(self._get_style('inputs.font_size', 10))
        font_spin.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.PlusMinus)
        font_spin.valueChanged.connect(lambda: self._update_input_preview())
        self.style_inputs['inputs.font_size'] = font_spin
        controls_layout.addRow("Font Size (pt):", font_spin)
        
        # Border width
        border_spin = QSpinBox()
        border_spin.setRange(0, 10)
        border_spin.setValue(self._get_style('inputs.border_width', 1))
        border_spin.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.PlusMinus)
        border_spin.valueChanged.connect(lambda: self._update_input_preview())
        self.style_inputs['inputs.border_width'] = border_spin
        controls_layout.addRow("Border Width (px):", border_spin)
        
        # Focus border width
        focus_border_spin = QSpinBox()
        focus_border_spin.setRange(0, 10)
        focus_border_spin.setValue(self._get_style('inputs.focus_border_width', 2))
        focus_border_spin.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.PlusMinus)
        focus_border_spin.valueChanged.connect(lambda: self._update_input_preview())
        self.style_inputs['inputs.focus_border_width'] = focus_border_spin
        controls_layout.addRow("Focus Border Width (px):", focus_border_spin)
        
        main_layout.addLayout(controls_layout)
        main_layout.addStretch(1)  # Add stretch between controls and preview
        
        # Preview on right
        preview_layout = QVBoxLayout()
        preview_layout.addWidget(QLabel("Preview:"))
        
        preview_input = QLineEdit("Input Preview")
        preview_input.setFixedSize(150, 30)
        self.preview_widgets['input'] = preview_input
        preview_layout.addWidget(preview_input)
        preview_layout.addStretch()
        
        main_layout.addLayout(preview_layout)
        
        group.setLayout(main_layout)
        parent_layout.addWidget(group)
        
        # Initial update
        self._update_input_preview()
    
    def _create_card_styles_section(self, parent_layout):
        """Create card styles section with preview on right"""
        group = QGroupBox("Card Styles")
        main_layout = QHBoxLayout()
        
        # Controls on left
        controls_layout = QFormLayout()
        
        # Border radius
        radius_spin = QSpinBox()
        radius_spin.setRange(0, 50)
        radius_spin.setValue(self._get_style('cards.border_radius', 8))
        radius_spin.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.PlusMinus)
        radius_spin.valueChanged.connect(lambda: self._update_card_preview())
        self.style_inputs['cards.border_radius'] = radius_spin
        controls_layout.addRow("Border Radius (px):", radius_spin)
        
        # Padding
        pad_spin = QSpinBox()
        pad_spin.setRange(0, 50)
        pad_spin.setValue(self._get_style('cards.padding', 12))
        pad_spin.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.PlusMinus)
        pad_spin.valueChanged.connect(lambda: self._update_card_preview())
        self.style_inputs['cards.padding'] = pad_spin
        controls_layout.addRow("Padding (px):", pad_spin)
        
        # Border width
        border_spin = QSpinBox()
        border_spin.setRange(0, 10)
        border_spin.setValue(self._get_style('cards.border_width', 0))
        border_spin.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.PlusMinus)
        border_spin.valueChanged.connect(lambda: self._update_card_preview())
        self.style_inputs['cards.border_width'] = border_spin
        controls_layout.addRow("Border Width (px):", border_spin)
        
        main_layout.addLayout(controls_layout)
        main_layout.addStretch(1)  # Add stretch between controls and preview
        
        # Preview on right
        preview_layout = QVBoxLayout()
        preview_layout.addWidget(QLabel("Preview:"))
        
        preview_card = QFrame()
        preview_card.setFixedSize(150, 80)
        card_label = QLabel("Card\nPreview")
        card_label.setAlignment(Qt.AlignCenter)
        card_layout = QVBoxLayout(preview_card)
        card_layout.addWidget(card_label)
        self.preview_widgets['card'] = preview_card
        preview_layout.addWidget(preview_card)
        preview_layout.addStretch()
        
        main_layout.addLayout(preview_layout)
        
        group.setLayout(main_layout)
        parent_layout.addWidget(group)
        
        # Initial update
        self._update_card_preview()
    
    def _create_label_styles_section(self, parent_layout):
        """Create label styles section with preview on right"""
        group = QGroupBox("Label Styles")
        main_layout = QHBoxLayout()
        
        # Controls on left
        controls_layout = QFormLayout()
        
        # Primary font size
        primary_font_spin = QSpinBox()
        primary_font_spin.setRange(6, 32)
        primary_font_spin.setValue(self._get_style('labels.font_size_primary', 14))
        primary_font_spin.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.PlusMinus)
        primary_font_spin.valueChanged.connect(lambda: self._update_label_preview())
        self.style_inputs['labels.font_size_primary'] = primary_font_spin
        controls_layout.addRow("Primary Font Size (pt):", primary_font_spin)
        
        # Secondary font size
        secondary_font_spin = QSpinBox()
        secondary_font_spin.setRange(6, 32)
        secondary_font_spin.setValue(self._get_style('labels.font_size_secondary', 10))
        secondary_font_spin.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.PlusMinus)
        secondary_font_spin.valueChanged.connect(lambda: self._update_label_preview())
        self.style_inputs['labels.font_size_secondary'] = secondary_font_spin
        controls_layout.addRow("Secondary Font Size (pt):", secondary_font_spin)
        
        main_layout.addLayout(controls_layout)
        main_layout.addStretch(1)  # Add stretch between controls and preview
        
        # Preview on right
        preview_layout = QVBoxLayout()
        preview_layout.addWidget(QLabel("Preview:"))
        
        primary_label = QLabel("Primary Label")
        primary_label.setObjectName("primary_label")
        self.preview_widgets['label_primary'] = primary_label
        preview_layout.addWidget(primary_label)
        
        secondary_label = QLabel("Secondary Label")
        secondary_label.setObjectName("secondary_label")
        self.preview_widgets['label_secondary'] = secondary_label
        preview_layout.addWidget(secondary_label)
        preview_layout.addStretch()
        
        main_layout.addLayout(preview_layout)
        
        group.setLayout(main_layout)
        parent_layout.addWidget(group)
        
        # Initial update
        self._update_label_preview()
    
    def _get_style(self, path, default=0):
        """Get style value from control styles"""
        style_data = self.parent_dialog.get_style_data()
        
        parts = path.split('.')
        value = style_data
        for part in parts:
            if isinstance(value, dict) and part in value:
                value = value[part]
            else:
                return default
        
        return value
    
    def _update_button_preview(self):
        """Update button preview with current style values"""
        if 'button' not in self.preview_widgets:
            return
        
        border_radius = self.style_inputs['buttons.border_radius'].value()
        pad_h = self.style_inputs['buttons.padding_horizontal'].value()
        pad_v = self.style_inputs['buttons.padding_vertical'].value()
        font_size = self.style_inputs['buttons.font_size'].value()
        border_width = self.style_inputs['buttons.border_width'].value()
        
        self.preview_widgets['button'].setStyleSheet(f"""
            QPushButton {{
                border-radius: {border_radius}px;
                padding: {pad_v}px {pad_h}px;
                font-size: {font_size}pt;
                border-width: {border_width}px;
            }}
        """)
    
    def _update_input_preview(self):
        """Update input preview with current style values"""
        if 'input' not in self.preview_widgets:
            return
        
        border_radius = self.style_inputs['inputs.border_radius'].value()
        pad_h = self.style_inputs['inputs.padding_horizontal'].value()
        pad_v = self.style_inputs['inputs.padding_vertical'].value()
        font_size = self.style_inputs['inputs.font_size'].value()
        border_width = self.style_inputs['inputs.border_width'].value()
        
        self.preview_widgets['input'].setStyleSheet(f"""
            QLineEdit {{
                border-radius: {border_radius}px;
                padding: {pad_v}px {pad_h}px;
                font-size: {font_size}pt;
                border-width: {border_width}px;
            }}
        """)
    
    def _update_card_preview(self):
        """Update card preview with current style values"""
        if 'card' not in self.preview_widgets:
            return
        
        border_radius = self.style_inputs['cards.border_radius'].value()
        padding = self.style_inputs['cards.padding'].value()
        border_width = self.style_inputs['cards.border_width'].value()
        
        self.preview_widgets['card'].setStyleSheet(f"""
            QFrame {{
                border-radius: {border_radius}px;
                padding: {padding}px;
                border-width: {border_width}px;
                border-style: solid;
                background: rgba(100, 100, 100, 50);
            }}
        """)
    
    def _update_label_preview(self):
        """Update label previews with current style values"""
        if 'label_primary' not in self.preview_widgets:
            return
        
        primary_size = self.style_inputs['labels.font_size_primary'].value()
        secondary_size = self.style_inputs['labels.font_size_secondary'].value()
        
        self.preview_widgets['label_primary'].setStyleSheet(f"font-size: {primary_size}pt;")
        self.preview_widgets['label_secondary'].setStyleSheet(f"font-size: {secondary_size}pt;")
    
    def get_style_data(self):
        """Get the current style data with user changes"""
        style_data = self.parent_dialog.get_style_data()
        
        # Update with current values
        for path, widget in self.style_inputs.items():
            parts = path.split('.')
            current = style_data
            for part in parts[:-1]:
                if part not in current:
                    current[part] = {}
                current = current[part]
            current[parts[-1]] = widget.value()
        
        return style_data
