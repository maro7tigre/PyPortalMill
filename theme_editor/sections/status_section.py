"""
Components Section
Status Cards and specialized components.
"""

from PySide6.QtWidgets import QComboBox, QLabel, QHBoxLayout
from ..base_section import ThemeEditorSection
from widgets.components.cards import StatusCard

class StatusSection(ThemeEditorSection):
    def setup_config_ui(self):
        # Neutral
        self.add_header("Neutral State")
        self.add_color_control("Background", "status_card.neutral.background", "#44475c")
        self.add_color_control("Border/Bar", "status_card.neutral.border", "#8b95c0")
        self.add_number_control("Title Size (px)", "status_card.neutral.title_size", 14, 8, 30)
        self.add_color_control("Title Color", "status_card.neutral.title_color", "#ffffff")
        self.add_number_control("Msg Size (px)", "status_card.neutral.msg_size", 11, 8, 30)
        self.add_color_control("Msg Color", "status_card.neutral.msg_color", "#8b95c0")
        
        # Valid
        self.add_header("Valid State")
        self.add_color_control("Background", "status_card.valid.background", "#1A2E20")
        self.add_color_control("Border/Bar", "status_card.valid.border", "#23c87b")
        self.add_number_control("Title Size (px)", "status_card.valid.title_size", 14, 8, 30)
        self.add_color_control("Title Color", "status_card.valid.title_color", "#ffffff")
        self.add_number_control("Msg Size (px)", "status_card.valid.msg_size", 11, 8, 30)
        self.add_color_control("Msg Color", "status_card.valid.msg_color", "#23c87b")
        
        # Changed
        self.add_header("Changed State")
        self.add_color_control("Background", "status_card.changed.background", "#3E2723")
        self.add_color_control("Border/Bar", "status_card.changed.border", "#FF9800")
        self.add_number_control("Title Size (px)", "status_card.changed.title_size", 14, 8, 30)
        self.add_color_control("Title Color", "status_card.changed.title_color", "#ffffff")
        self.add_number_control("Msg Size (px)", "status_card.changed.msg_size", 11, 8, 30)
        self.add_color_control("Msg Color", "status_card.changed.msg_color", "#FF9800")

    def setup_preview_ui(self):
        layout = self.preview_inner_layout
        
        self.card = StatusCard("Status", "Message")
        layout.addWidget(self.card)
        
        # State selector for preview
        combo = QComboBox()
        combo.addItems(["Neutral", "Valid", "Changed"])
        combo.currentTextChanged.connect(lambda s: self.card.set_state(s.lower()))
        layout.addWidget(QLabel("Preview State:"))
        layout.addWidget(combo)
        
        layout.addStretch()
