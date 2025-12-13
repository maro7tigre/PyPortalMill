"""
Cards & Layouts Section
Configuration for Cards (Profiles, Types) and Collection Layouts.
"""

from PySide6.QtWidgets import QVBoxLayout, QLabel
from ..base_section import ThemeEditorSection
from widgets.items import ProfileItem, TypeItem
from widgets.collections import ProfileGrid, TypeSelector

class ContainersSection(ThemeEditorSection):
    def setup_config_ui(self):
        # --- CARDS ---
        self.add_header("Cards - Dimensions")
        self.add_number_control("Width (px)", "control_styles.cards.width", 120, 50, 300)
        self.add_number_control("Height (px)", "control_styles.cards.height", 140, 50, 300)
        self.add_number_control("Image Size (px)", "control_styles.cards.image_size", 100, 20, 200)
        self.add_number_control("Font Size (px)", "control_styles.cards.font_size", 12, 6, 24)
        self.add_number_control("Border Radius (px)", "control_styles.cards.border_radius", 4, 0, 50)
        self.add_number_control("Border Width (px)", "control_styles.cards.border_width", 2, 0, 10)

        self.add_header("Cards - Neutral State")
        self.add_color_control("Background", "cards.neutral.background", "#44475c")
        self.add_color_control("Border", "cards.neutral.border", "#6f779a")
        self.add_color_control("Text", "cards.neutral.text", "#ffffff") # Optional if label uses generic text color

        self.add_header("Cards - Hovered State")
        self.add_color_control("Background", "cards.hovered.background", "#3a3d4d")
        self.add_color_control("Border", "cards.hovered.border", "#8b95c0")
        
        self.add_header("Cards - Selected State")
        self.add_color_control("Background", "cards.selected.background", "#1A2E20")
        self.add_color_control("Border", "cards.selected.border", "#23c87b")
        
        # --- LAYOUTS ---
        self.add_header("Layouts - Profile Grid")
        self.add_color_control("Background", "layouts.profile_grid.background", "#282a36")
        self.add_color_control("Border", "layouts.profile_grid.border", "#44475c")
        # self.add_number_control("Spacing", "layouts.profile_grid.spacing", 10, 0, 50) # If implemented in grid layout update

        self.add_header("Layouts - Type Selector")
        self.add_color_control("Background", "layouts.type_selector.background", "#1d1f28")
        # self.add_number_control("Spacing", "layouts.type_selector.spacing", 10, 0, 50)

    def setup_preview_ui(self):
        from PySide6.QtWidgets import QTabWidget, QWidget
        layout = self.preview_inner_layout
        
        tab_widget = QTabWidget()
        layout.addWidget(tab_widget)
        
        # Tab 1: Single Card
        tab1 = QWidget()
        l1 = QVBoxLayout(tab1)
        l1.addWidget(QLabel("Single Profile Card:"))
        self.card_preview = ProfileItem("Preview Profile")
        l1.addWidget(self.card_preview)
        l1.addStretch()
        tab_widget.addTab(tab1, "Single Card")
        
        # Tab 2: Grid Layout
        tab2 = QWidget()
        l2 = QVBoxLayout(tab2)
        l2.addWidget(QLabel("Profile Grid Layout:"))
        self.grid_preview = ProfileGrid("preview")
        self.grid_preview.update_profiles({
            "Profile 1": {}, "Profile 2": {}
        })
        l2.addWidget(self.grid_preview)
        tab_widget.addTab(tab2, "Grid Layout")
        
        # Tab 3: Selector Layout
        tab3 = QWidget()
        l3 = QVBoxLayout(tab3)
        l3.addWidget(QLabel("Type Selector Layout:"))
        self.type_preview = TypeSelector("preview")
        self.type_preview.load_types({
            "Type A": {"name": "Type A", "image": None}, 
            "Type B": {"name": "Type B", "image": None}
        })
        l3.addWidget(self.type_preview)
        l3.addStretch()
        tab_widget.addTab(tab3, "Type Selector")

    def update_preview(self):
        # Force styles update on widgets if they don't auto-update via some signal
        # The widgets usually listen to signals or need re-polish.
        # But since we use ThemeManager which emits signals, they *should* update if they listen.
        # ProfileGrid/TypeSelector might need a full repaint or re-style.
        
        if hasattr(self, 'card_preview'):
            self.card_preview.update_style()
        
        # Trigger updates on items inside grid/selector if possible. 
        # But usually ThemeManager signal handles it globally if widgets listen.
        # Currently CardItem doesn't listen to ThemeManager signal automatically unless we connect it.
        # Check CardItem implementation: it does NOT connect to theme_changed. 
        # We might need to manually trigger update_style here for the preview instance.
        pass
