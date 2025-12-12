from PySide6.QtWidgets import QGroupBox, QScrollArea, QSplitter, QListWidget, QMenu
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

class ThemedListWidget(QListWidget, ThemedWidgetMixin):
    """Dark themed list widget"""
    def __init__(self, parent=None):
        super().__init__(parent)
        ThemedWidgetMixin.__init__(self)
        self.setStyleSheet("""
            QListWidget {
                background-color: #1d1f28;
                color: #ffffff;
                border: 1px solid #6f779a;
                border-radius: 4px;
                padding: 4px;
                outline: none;
            }
            QListWidget::item {
                background-color: #44475c;
                border: 1px solid #6f779a;
                border-radius: 3px;
                padding: 6px;
                margin: 2px;
            }
            QListWidget::item:selected {
                background-color: #BB86FC;
                color: #1d1f28;
                border: 1px solid #BB86FC;
            }
            QListWidget::item:hover {
                background-color: #6f779a;
                border: 1px solid #8b95c0;
            }
        """)

class ThemedMenu(QMenu, ThemedWidgetMixin):
    """Dark themed context menu"""
    def __init__(self, parent=None):
        super().__init__(parent)
        ThemedWidgetMixin.__init__(self)

