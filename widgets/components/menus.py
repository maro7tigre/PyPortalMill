from PySide6.QtWidgets import QMenu
from widgets.mixins import ThemedWidgetMixin

class ThemedMenu(QMenu, ThemedWidgetMixin):
    def __init__(self, parent=None):
        super().__init__(parent)
        ThemedWidgetMixin.__init__(self)
