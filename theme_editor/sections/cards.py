from PySide6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QLabel, QTabWidget, QWidget, QPushButton, QFrame, QScrollArea, QSplitter
)
from PySide6.QtCore import Qt
from ..base_section import ThemeEditorSection
from widgets.components.cards import ProfileItem, TypeItem
from widgets.components.lists import ProfileGrid, TypeSelector

class CardsSection(ThemeEditorSection):
    def setup_config_ui(self):
        # Top level tabs: Profiles vs Types
        self.main_tabs = QTabWidget()
        self.config_layout.addWidget(self.main_tabs)
        
        self._setup_profile_tab()
        self._setup_type_tab()
        
    def _setup_profile_tab(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        # Scroll area for the page content if needed, but config_layout is already scrollable.
        # However, nesting scrollables can be tricky. We'll just add to layout.
        
        prefix = "cards.profile"
        layout_prefix = "layouts.profile_grid"
        
        # 1. Dimensions
        self._add_header(layout, "Profile Card Dimensions")
        self._add_inline_size_control(layout, "Card Size", f"control_styles.{prefix}.width", f"control_styles.{prefix}.height", 120, 140)
        self._add_inline_size_control(layout, "Image Size", f"control_styles.{prefix}.image_size_w", f"control_styles.{prefix}.image_size_h", 100, 100)
        self._add_num(layout, "Font Size (pt)", f"control_styles.{prefix}.font_size", 12, 6, 24)
        
        # 2. Styling States
        self._add_header(layout, "Card Styling")
        self._add_state_tabs(layout, prefix)
        
        # 3. Layout Styling
        self._add_header(layout, "Grid Layout")
        self._add_color(layout, "Background", f"control_styles.{layout_prefix}.background", "#282a36")
        self._add_color(layout, "Border", f"control_styles.{layout_prefix}.border", "#44475c")
        self._add_num(layout, "Minimum Spacing", f"control_styles.{layout_prefix}.spacing", 10, 0, 999)
        
        # Individual padding controls
        self._add_header(layout, "Grid Padding")
        self._add_num(layout, "Padding Top", f"control_styles.{layout_prefix}.padding_top", 10, 0, 999)
        self._add_num(layout, "Padding Right", f"control_styles.{layout_prefix}.padding_right", 10, 0, 999)
        self._add_num(layout, "Padding Bottom", f"control_styles.{layout_prefix}.padding_bottom", 10, 0, 999)
        self._add_num(layout, "Padding Left", f"control_styles.{layout_prefix}.padding_left", 10, 0, 999)
        
        layout.addStretch()
        self.main_tabs.addTab(page, "Profiles")

    def _setup_type_tab(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        
        prefix = "cards.type"
        layout_prefix = "layouts.type_selector"
        
        # 1. Dimensions
        self._add_header(layout, "Type Card Dimensions")
        self._add_inline_size_control(layout, "Card Size", f"control_styles.{prefix}.width", f"control_styles.{prefix}.height", 100, 120)
        self._add_inline_size_control(layout, "Image Size", f"control_styles.{prefix}.image_size_w", f"control_styles.{prefix}.image_size_h", 80, 80)
        self._add_num(layout, "Font Size (pt)", f"control_styles.{prefix}.font_size", 10, 6, 24)
        
        # 2. Styling States
        self._add_header(layout, "Card Styling")
        self._add_state_tabs(layout, prefix)
        
        # 3. Layout Styling
        self._add_header(layout, "Selector Layout")
        self._add_color(layout, "Background", f"control_styles.{layout_prefix}.background", "#1d1f28")
        self._add_color(layout, "Border", f"control_styles.{layout_prefix}.border", "#44475c")
        self._add_num(layout, "Spacing", f"control_styles.{layout_prefix}.spacing", 10, 0, 999)
        
        # Individual padding controls
        self._add_header(layout, "Selector Padding")
        self._add_num(layout, "Padding Top", f"control_styles.{layout_prefix}.padding_top", 5, 0, 999)
        self._add_num(layout, "Padding Right", f"control_styles.{layout_prefix}.padding_right", 5, 0, 999)
        self._add_num(layout, "Padding Bottom", f"control_styles.{layout_prefix}.padding_bottom", 5, 0, 999)
        self._add_num(layout, "Padding Left", f"control_styles.{layout_prefix}.padding_left", 5, 0, 999)
        
        layout.addStretch()
        self.main_tabs.addTab(page, "Types")

    # --- Helpers ---
    
    def _add_state_tabs(self, parent_layout, prefix):
        tabs = QTabWidget()
        parent_layout.addWidget(tabs)
        
        states = [
            ("Normal", "neutral"),
            ("Hovered", "hovered"),
            ("Selected", "selected")
        ]
        
        defaults = {
            "neutral": {"bg": "#44475c", "border": "#6f779a"},
            "hovered": {"bg": "#3a3d4d", "border": "#8b95c0"},
            "selected": {"bg": "#1A2E20", "border": "#23c87b"}
        }
        
        for label, key in states:
            page = QWidget()
            layout = QVBoxLayout(page)
            layout.setContentsMargins(10, 10, 10, 10)
            
            d = defaults.get(key, defaults["neutral"])
            
            self._add_color(layout, "Background", f"{prefix}.{key}.background", d["bg"])
            self._add_color(layout, "Border Color", f"{prefix}.{key}.border", d["border"])
            self._add_color(layout, "Text Color", f"{prefix}.{key}.text", "#ffffff")
            
            layout.addSpacing(10)
            self._add_num(layout, "Border Radius", f"{prefix}.{key}.border_radius", 4, 0, 30)
            self._add_num(layout, "Border Width", f"{prefix}.{key}.border_width", 2, 0, 10)
            
            layout.addStretch()
            tabs.addTab(page, label)

    def _add_header(self, layout, title):
        lbl = QLabel(title)
        lbl.setStyleSheet("font-weight: bold; margin-top: 20px; margin-bottom: 5px; color: #BB86FC;")
        layout.addWidget(lbl)

    def _add_color(self, layout, name, path, default):
        row = QWidget()
        l = QHBoxLayout(row)
        l.setContentsMargins(0,0,0,0)
        l.addWidget(QLabel(name))
        l.addStretch()
        
        btn = QPushButton()
        btn.setFixedSize(60, 24)
        curr_val = self.get_style_value(path, default)
        btn.setStyleSheet(f"background-color: {curr_val}; border: 1px solid #666; border-radius: 4px;")
        btn.clicked.connect(lambda checked=False, p=path, b=btn: self._pick_color(p, b))
        
        l.addWidget(btn)
        layout.addWidget(row)

    def _add_num(self, layout, name, path, default, min_v, max_v):
        from PySide6.QtWidgets import QSpinBox
        row = QWidget()
        l = QHBoxLayout(row)
        l.setContentsMargins(0,0,0,0)
        l.addWidget(QLabel(name))
        l.addStretch()
        
        spin = QSpinBox()
        spin.setRange(min_v, max_v)
        curr_val = self.get_style_value(path, default)
        spin.setValue(int(curr_val))
        spin.valueChanged.connect(lambda v, p=path: self.set_theme_value(p, v))
        
        l.addWidget(spin)
        layout.addWidget(row)
        
    def _add_inline_size_control(self, layout, label, key_w, key_h, def_w, def_h):
        row = QWidget()
        l = QHBoxLayout(row)
        l.setContentsMargins(0, 5, 0, 5)
        
        l.addWidget(QLabel(label))
        l.addStretch()
        
        from PySide6.QtWidgets import QSpinBox
        
        # Width
        sb_w = QSpinBox()
        sb_w.setRange(10, 500)
        sb_w.setSuffix(" px")
        sb_w.setValue(int(self.get_style_value(key_w, def_w)))
        sb_w.valueChanged.connect(lambda v: self.set_theme_value(key_w, v))
        
        # Height
        sb_h = QSpinBox()
        sb_h.setRange(10, 500)
        sb_h.setSuffix(" px")
        sb_h.setValue(int(self.get_style_value(key_h, def_h)))
        sb_h.valueChanged.connect(lambda v: self.set_theme_value(key_h, v))
        
        l.addWidget(QLabel("W:"))
        l.addWidget(sb_w)
        l.addSpacing(10)
        l.addWidget(QLabel("H:"))
        l.addWidget(sb_h)
        
        layout.addWidget(row)

    def setup_preview_ui(self):
        layout = self.preview_inner_layout
        
        # We want to show ProfileGrid and TypeSelector to test layout/spacing/selection
        
        # Profile Section
        layout.addWidget(QLabel("Profile Grid Preview (Click to Select)"))
        
        self.profile_grid = ProfileGrid("Preview Profiles")
        self.profile_grid.setFixedHeight(300) # Limit height for scroll check? or let it expand
        
        # Populate with dummy
        self.profile_grid.update_profiles({
            "Standard Door": {},
            "Shaker Style": {},
            "Glass Panel": {},
            "Solid Wood": {}
        })
        layout.addWidget(self.profile_grid)
        
        layout.addSpacing(20)
        
        # Type Section
        layout.addWidget(QLabel("Type Selector Preview"))
        
        self.type_selector = TypeSelector("Preview Types")
        # Self-sizing based on content
        # self.type_selector.setFixedHeight(150)
        
        self.type_selector.load_types({
            "Single": {"name": "Single"},
            "Double": {"name": "Double"},
            "Sliding": {"name": "Sliding"}
        })
        layout.addWidget(self.type_selector)
        
        layout.addStretch()

    def update_preview(self):
        # We need to force update styling on our preview widgets.
        # Since they don't auto-listen to theme_changed signal unless connected globally,
        # we might need to manually trigger their style updates or re-polish.
        # CardItem.update_style() pulls from ThemeManager directly. 
        # So we just need to repaint/update.
        
        # However, dimensions might need explicit update if they are cached in init.
        # CardItem.update_style now handles dimensions!
        
        # Iterate over children of grids to force update might be needed if they don't auto-update.
        # ProfileGrid/TypeSelector structure:
        # they contain SelectableItems.
        
        # Let's define a helper to refresh interactions
        def refresh_grid(grid):
            # Hack/Fix: iterate children or rely on widget update
            # Since update_style is called in paintEvent or via signal? 
            # CardItem calls update_style() in constructor.
            # We need to call it again.
            children = grid.findChildren(ProfileItem) + grid.findChildren(TypeItem)
            for child in children:
                child.update_style()
                
            # Also update grid/selector background if they support it
            # ProfileGrid/TypeSelector don't seem to have update_style method exposed in previous step?
            # We should check widgets/components/lists.py if they have ThemedWidgetMixin and update_style.
            if hasattr(grid, 'update_style'):
                 grid.update_style() # Only if implemented
            else:
                # Manual stylesheet update for container
                 pass
        
        if hasattr(self, 'profile_grid'):
            refresh_grid(self.profile_grid)
            
        if hasattr(self, 'type_selector'):
            refresh_grid(self.type_selector)
