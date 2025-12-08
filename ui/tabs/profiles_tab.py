"""
Profiles Tab - Placeholder for profile selection
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt


class ProfilesTab(QWidget):
    """Placeholder tab for Profiles section"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup the UI"""
        layout = QVBoxLayout(self)
        
        label = QLabel("Profiles Tab - Coming Soon")
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("font-size: 16pt; font-weight: bold;")
        
        layout.addWidget(label)
