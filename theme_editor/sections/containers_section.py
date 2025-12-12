"""
Containers Section
Configuration for Cards, GroupBoxes, etc.
"""

from PySide6.QtWidgets import QLabel, QVBoxLayout
from ..base_section import ThemeEditorSection
from widgets.primitives.containers import ThemedGroupBox

class ContainersSection(ThemeEditorSection):
    def setup_config_ui(self):
        self.add_header("Cards")
        self.add_number_control("Border Radius (px)", "styles.cards.border_radius", 8, 0, 50)
        self.add_number_control("Padding (px)", "styles.cards.padding", 12, 0, 50)
        self.add_number_control("Border Width (px)", "styles.cards.border_width", 0, 0, 10)
        
        self.add_header("Group Boxes")
        # Add group box styling if exposed in theme manager/stylesheets settings
        # Currently standard QGroupBox might use platform style or simple stylesheet
        pass

    def setup_preview_ui(self):
        layout = self.preview_inner_layout
        
        grp = ThemedGroupBox("Group Box Title")
        l = QVBoxLayout(grp)
        l.addWidget(QLabel("Content inside group box"))
        layout.addWidget(grp)
        
        # We need a generic card preview. 
        # Since 'CardItem' is a complex widget, maybe we just use a Frame with card style?
        # Or better yet, import ProfileItem as an example of a Card.
        from widgets.components.cards import ProfileItem
        layout.addWidget(ProfileItem("Sample Card"))
        
        layout.addStretch()
