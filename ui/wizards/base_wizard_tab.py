"""
Base Wizard Tab

Reusable 3-step wizard system for both Doors and Frames contexts.

Steps:
1. Profiles/Selection - Select hardware profiles (hinges, locks)
2. Setup/Configure - Configure parameters and preview
3. Export/Generate - Generate and export G-code files
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QStackedWidget,
                             QLabel, QFrame)
from PySide6.QtCore import Qt, Signal
from ui.widgets import ThemedButton, ThemedLabel


class BaseWizardTab(QWidget):
    """
    Base wizard with 3 steps that can be inherited by Doors and Frames tabs.
    
    The wizard provides a consistent navigation flow with step indicators
    and automatic validation between steps.
    """
    
    # Signals
    step_changed = Signal(int)  # Emitted when step changes
    wizard_completed = Signal()  # Emitted when wizard is completed
    
    def __init__(self, context: str, parent=None):
        """
        Initialize the base wizard.
        
        Args:
            context: "doors" or "frames" - determines which parameters/profiles to use
            parent: Parent widget
        """
        super().__init__(parent)
        self.context = context
        self.current_step = 0
        self.total_steps = 3
        
        # Step widgets will be set by subclass or created here
        self.selection_step = None
        self.configure_step = None
        self.generate_step = None
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the wizard UI with step indicator, content area, and navigation"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Step indicator at top
        self.step_indicator = self.create_step_indicator()
        layout.addWidget(self.step_indicator)
        
        # Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        layout.addWidget(separator)
        
        # Stacked widget for step content
        self.step_stack = QStackedWidget()
        layout.addWidget(self.step_stack, 1)
        
        # Navigation buttons at bottom
        nav_layout = self.create_navigation()
        layout.addLayout(nav_layout)
    
    def create_step_indicator(self) -> QWidget:
        """Create the step indicator widget showing current progress"""
        indicator = QWidget()
        layout = QHBoxLayout(indicator)
        layout.setContentsMargins(20, 10, 20, 10)
        
        self.step_labels = []
        step_names = [
            "1. Profiles/Selection",
            "2. Setup/Configure",
            "3. Export/Generate"
        ]
        
        for i, name in enumerate(step_names):
            if i > 0:
                # Add arrow between steps
                arrow = ThemedLabel("→")
                layout.addWidget(arrow)
            
            step_label = ThemedLabel(name)
            step_label.setAlignment(Qt.AlignCenter)
            self.step_labels.append(step_label)
            layout.addWidget(step_label)
        
        layout.addStretch()
        
        self.update_step_indicator()
        return indicator
    
    def update_step_indicator(self):
        """Update step indicator to highlight current step"""
        for i, label in enumerate(self.step_labels):
            if i == self.current_step:
                # Current step - bold and accent color
                label.setStyleSheet("font-weight: bold; font-size: 11pt;")
            elif i < self.current_step:
                # Completed steps - normal style
                label.setStyleSheet("font-size: 10pt;")
            else:
                # Future steps - dimmed
                label.setStyleSheet("font-size: 10pt; color: gray;")
    
    def create_navigation(self) -> QHBoxLayout:
        """Create navigation buttons (Back/Next/Finish)"""
        nav_layout = QHBoxLayout()
        nav_layout.setContentsMargins(20, 10, 20, 10)
        
        # Back button
        self.back_button = ThemedButton("← Back", button_type="secondary")
        self.back_button.clicked.connect(self.prev_step)
        nav_layout.addWidget(self.back_button)
        
        nav_layout.addStretch()
        
        # Next/Finish button
        self.next_button = ThemedButton("Next →", button_type="primary")
        self.next_button.clicked.connect(self.next_step)
        nav_layout.addWidget(self.next_button)
        
        self.update_navigation_buttons()
        return nav_layout
    
    def update_navigation_buttons(self):
        """Update navigation button states based on current step"""
        # Back button disabled on first step
        self.back_button.setEnabled(self.current_step > 0)
        
        # Change Next to Finish on last step
        if self.current_step == self.total_steps - 1:
            self.next_button.setText("Finish ✓")
        else:
            self.next_button.setText("Next →")
    
    def set_step_widgets(self, selection_step, configure_step, generate_step):
        """
        Set the step widgets (to be called by subclass).
        
        Args:
            selection_step: Widget for step 1 (Profiles/Selection)
            configure_step: Widget for step 2 (Setup/Configure)
            generate_step: Widget for step 3 (Export/Generate)
        """
        self.selection_step = selection_step
        self.configure_step = configure_step
        self.generate_step = generate_step
        
        # Add to stacked widget
        self.step_stack.addWidget(self.selection_step)
        self.step_stack.addWidget(self.configure_step)
        self.step_stack.addWidget(self.generate_step)
        
        # Show first step
        self.step_stack.setCurrentIndex(0)
    
    def next_step(self):
        """Move to next step with validation"""
        # Validate current step before proceeding
        if not self.validate_current_step():
            return
        
        if self.current_step < self.total_steps - 1:
            self.current_step += 1
            self.step_stack.setCurrentIndex(self.current_step)
            self.update_step_indicator()
            self.update_navigation_buttons()
            self.step_changed.emit(self.current_step)
        else:
            # On last step, finish wizard
            self.finish_wizard()
    
    def prev_step(self):
        """Move to previous step"""
        if self.current_step > 0:
            self.current_step -= 1
            self.step_stack.setCurrentIndex(self.current_step)
            self.update_step_indicator()
            self.update_navigation_buttons()
            self.step_changed.emit(self.current_step)
    
    def validate_current_step(self) -> bool:
        """
        Validate current step before moving to next.
        Override in subclass for specific validation logic.
        
        Returns:
            True if validation passes, False otherwise
        """
        # Default: no validation, always pass
        # Subclasses should override this
        return True
    
    def finish_wizard(self):
        """Called when wizard is completed (Finish button clicked)"""
        self.wizard_completed.emit()
    
    def goto_step(self, step_index: int):
        """Jump to a specific step (0-indexed)"""
        if 0 <= step_index < self.total_steps:
            self.current_step = step_index
            self.step_stack.setCurrentIndex(step_index)
            self.update_step_indicator()
            self.update_navigation_buttons()
            self.step_changed.emit(self.current_step)
    
    def reset_wizard(self):
        """Reset wizard to first step"""
        self.goto_step(0)
