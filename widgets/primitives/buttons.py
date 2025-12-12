from PySide6.QtWidgets import QPushButton
from widgets.mixins import ThemedWidgetMixin

class ThemedButton(QPushButton, ThemedWidgetMixin):
    """Base themed button"""
    def __init__(self, text="", theme_class="neutral", parent=None):
        super().__init__(text, parent)
        ThemedWidgetMixin.__init__(self)
        self.setProperty("class", theme_class)
        # Ensure property change triggers style update
        self.style().unpolish(self)
        self.style().polish(self)

class PurpleButton(ThemedButton):
    """Primary Action Button"""
    def __init__(self, text="", parent=None):
        super().__init__(text, "primary", parent)

class GreenButton(ThemedButton):
    """Success/Confirmation Button"""
    def __init__(self, text="", parent=None):
        super().__init__(text, "success", parent)

class BlueButton(ThemedButton):
    """Secondary Action Button"""
    def __init__(self, text="", parent=None):
        super().__init__(text, "secondary", parent)

class OrangeButton(ThemedButton):
    """Warning/Export Button"""
    def __init__(self, text="", parent=None):
        super().__init__(text, "tertiary", parent)

class DangerButton(ThemedButton):
    """Destructive Action Button"""
    def __init__(self, text="", parent=None):
        super().__init__(text, "danger", parent)
