from PySide6.QtWidgets import QHBoxLayout, QPushButton, QTabWidget, QWidget, QVBoxLayout, QLabel
from ..base_section import ThemeEditorSection
from widgets.primitives.buttons import PurpleButton, GreenButton, BlueButton, OrangeButton, DangerButton, ThemedButton

class ButtonsSection(ThemeEditorSection):
    def setup_config_ui(self):
        # Global Dimensions
        self.add_header("Global Dimensions")
        self.add_number_control("Border Radius (px)", "styles.buttons.border_radius", 4, 0, 30)
        self.add_number_control("Padding Horizontal (px)", "styles.buttons.padding_horizontal", 12, 0, 50)
        self.add_number_control("Padding Vertical (px)", "styles.buttons.padding_vertical", 6, 0, 30)
        self.add_number_control("Border Width (px)", "styles.buttons.border_width", 1, 0, 10)
        self.add_number_control("Font Size (pt)", "styles.buttons.font_size", 10, 6, 30)
        
        # Tabs for Button Types
        self.add_header("Button Colors by Type")
        tabs = QTabWidget()
        
        # Define types to edit
        types = [
            ("Neutral", "neutral"),
            ("Primary", "primary"),
            ("Success", "success"),
            ("Warning", "tertiary"), # Mapped to OrangeButton usually
            ("Danger", "danger")
        ]
        
        for label, key in types:
            page = QWidget()
            layout = QVBoxLayout(page)
            layout.setContentsMargins(5, 5, 5, 5)
            
            # Helper to add section inside tab
            def add_state_controls(state_name, state_key):
                l = QLabel(state_name)
                l.setStyleSheet("font-weight: bold; margin-top: 10px;")
                layout.addWidget(l)
                
                # We need to access the parent section's add_color_control logic
                # But add_color_control adds to self.config_layout directly.
                # We need a custom helper here to add to 'layout'
                
                rows = [
                    ("Background", "background"),
                    ("Text", "text"),
                    ("Outline", "outline")
                ]
                
                for row_label, row_key in rows:
                    full_path = f"buttons.{key}.{state_key}.{row_key}"
                    
                    # Create row manually
                    row_w = QWidget()
                    row_l = QHBoxLayout(row_w)
                    row_l.setContentsMargins(0, 0, 0, 0)
                    row_l.addWidget(QLabel(row_label))
                    row_l.addStretch()
                    
                    btn = QPushButton()
                    btn.setFixedSize(50, 20)
                    current_val = self.get_style_value(full_path, "#000000")
                    btn.setStyleSheet(f"background-color: {current_val}; border: 1px solid #666;")
                    btn.clicked.connect(lambda checked=False, p=full_path, b=btn: self._pick_color(p, b))
                    
                    row_l.addWidget(btn)
                    layout.addWidget(row_w)

            add_state_controls("Normal", "normal")
            add_state_controls("Hover", "hovered")
            add_state_controls("Pressed", "clicked")
            add_state_controls("Disabled", "disabled")
            
            layout.addStretch()
            tabs.addTab(page, label)
            
        self.config_layout.addWidget(tabs)

    def setup_preview_ui(self):
        layout = self.preview_inner_layout
        
        from PySide6.QtWidgets import QCheckBox
        
        def add_preview_row(label, widget):
            row = QWidget()
            row_layout = QHBoxLayout(row)
            row_layout.setContentsMargins(0, 5, 0, 5)
            
            # Left side: Label + Button
            left = QWidget()
            left_l = QVBoxLayout(left)
            left_l.setContentsMargins(0,0,0,0)
            left_l.addWidget(QLabel(label))
            left_l.addWidget(widget)
            
            # Right side: Checkbox
            cb = QCheckBox("Disabled")
            cb.toggled.connect(lambda checked: widget.setDisabled(checked))
            
            row_layout.addWidget(left)
            row_layout.addStretch()
            row_layout.addWidget(cb)
            
            layout.addWidget(row)

        add_preview_row("Neutral", QPushButton("Neutral Action"))
        add_preview_row("Primary", PurpleButton("Primary Action"))
        add_preview_row("Success", GreenButton("Success Action"))
        add_preview_row("Warning (Tertiary)", OrangeButton("Warning Action"))
        add_preview_row("Danger", DangerButton("Destructive Action"))
        
        layout.addStretch()
 
