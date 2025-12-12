from PySide6.QtWidgets import QLineEdit, QTextEdit, QSpinBox, QDoubleSpinBox, QCheckBox, QRadioButton
from widgets.mixins import ThemedWidgetMixin


class ThemedCheckBox(QCheckBox, ThemedWidgetMixin):
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        ThemedWidgetMixin.__init__(self)

class ThemedRadioButton(QRadioButton, ThemedWidgetMixin):
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        ThemedWidgetMixin.__init__(self)

class ThemedLineEdit(QLineEdit, ThemedWidgetMixin):
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        ThemedWidgetMixin.__init__(self)

class ErrorLineEdit(ThemedLineEdit):
    """LineEdit that can show error state"""
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self._has_error = False
        
    def set_error(self, has_error):
        self._has_error = has_error
        self.setProperty("error", has_error)
        self.style().unpolish(self)
        self.style().polish(self)
        
    def has_error(self):
        return self._has_error

class ThemedTextEdit(QTextEdit, ThemedWidgetMixin):
    def __init__(self, parent=None):
        super().__init__(parent)
        ThemedWidgetMixin.__init__(self)

class ThemedSpinBox(QSpinBox, ThemedWidgetMixin):
    def __init__(self, parent=None):
        super().__init__(parent)
        ThemedWidgetMixin.__init__(self)

class ThemedDoubleSpinBox(QDoubleSpinBox, ThemedWidgetMixin):
    def __init__(self, parent=None):
        super().__init__(parent)
        ThemedWidgetMixin.__init__(self)
