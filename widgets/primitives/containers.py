from PySide6.QtWidgets import QGroupBox, QScrollArea, QSplitter
from PySide6.QtCore import Qt
from widgets.mixins import ThemedWidgetMixin

class ThemedGroupBox(QGroupBox, ThemedWidgetMixin):
    def __init__(self, title="", parent=None):
        super().__init__(title, parent)
        ThemedWidgetMixin.__init__(self)

class ThemedScrollArea(QScrollArea, ThemedWidgetMixin):
    def __init__(self, parent=None):
        super().__init__(parent)
        ThemedWidgetMixin.__init__(self)

class ThemedSplitter(QSplitter, ThemedWidgetMixin):
    def __init__(self, orientation=Qt.Horizontal, parent=None):
        super().__init__(orientation, parent)
        ThemedWidgetMixin.__init__(self)
