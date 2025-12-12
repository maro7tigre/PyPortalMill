"""
Components Section
Status Cards and specialized components.
"""

from PySide6.QtWidgets import QComboBox, QLabel, QHBoxLayout
from ..base_section import ThemeEditorSection
from widgets.components.cards import StatusCard

class StatusSection(ThemeEditorSection):
    def setup_config_ui(self):
        self.add_header("Status Card States")
        self.add_color_control("Valid State", "status_card.valid", "#23c87b")
        self.add_color_control("Changed State", "status_card.changed", "#ff8c00")
        self.add_color_control("Neutral State", "status_card.neutral", "#44475c")

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
