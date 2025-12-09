"""
Generate Step

Third step in the wizard: Generate and export G-code files.
Adapted from the old GenerateTab with exact same UI but integrated with new architecture.
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QFileDialog, QMessageBox
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
import os
import shutil

from ui.widgets import (ThemedSplitter, ThemedLabel, ThemedLineEdit, ThemedGroupBox,
                        PurpleButton, GreenButton, OrangeButton)


class GenerateStep(QWidget):
    """
    G-code generation step with exact same interface as old GenerateTab.
    
    Features:
    - Split view for left/right side files
    - For frames: 3 files per side (frame, lock, hinge)
    - For doors: 4 files per side (TBD)
    - Sync status indicators
    - Generate and Export buttons
    """
    
    def __init__(self, context: str, parent=None):
        """
        Initialize generate step.
        
        Args:
            context: "frames" or "doors" - determines number of files
            parent: Parent widget
        """
        super().__init__(parent)
        self.context = context
        self.output_dir = os.path.expanduser("~/CNC/Output")
        self.first_time_opened = True
        
        # File items organized by side and type
        self.file_items = {
            'left': {},
            'right': {}
        }
        
        self.setup_ui()
        self.connect_signals()
    
    def setup_ui(self):
        """Initialize user interface"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        # Top toolbar
        toolbar_layout = QHBoxLayout()
        main_layout.addLayout(toolbar_layout)
        
        # Title
        title_label = ThemedLabel("Generated G-Code Files")
        title_label.setFont(QFont("Arial", 14, QFont.Bold))
        toolbar_layout.addWidget(title_label)
        
        toolbar_layout.addStretch()
        
        # Generate button
        self.generate_button = GreenButton("Generate Files")
        toolbar_layout.addWidget(self.generate_button)
        
        # Main content area with splitter
        content_splitter = ThemedSplitter(Qt.Horizontal)
        main_layout.addWidget(content_splitter, 1)
        
        # Left side files
        left_widget = self.create_side_panel("Left Side", "left")
        content_splitter.addWidget(left_widget)
        
        # Right side files
        right_widget = self.create_side_panel("Right Side", "right")
        content_splitter.addWidget(right_widget)
        
        # Set equal sizes
        content_splitter.setSizes([400, 400])
        
        # Output directory section with export button
        output_layout = QHBoxLayout()
        main_layout.addLayout(output_layout)
        
        output_layout.addWidget(ThemedLabel("Output Directory:"))
        self.output_path = ThemedLineEdit(self.output_dir)
        self.output_path.setReadOnly(True)
        output_layout.addWidget(self.output_path)
        
        browse_button = PurpleButton("Browse")
        browse_button.clicked.connect(self.browse_output_dir)
        output_layout.addWidget(browse_button)
        
        # Export button
        self.export_button = OrangeButton("Export Files")
        self.export_button.clicked.connect(self.export_files)
        output_layout.addWidget(self.export_button)
    
    def create_side_panel(self, title, side):
        """Create a panel for left or right side files"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Group box
        group = ThemedGroupBox(title)
        group_layout = QVBoxLayout(group)
        layout.addWidget(group)
        
        # Determine file types based on context
        if self.context == "frames":
            file_types = [
                ('frame', f'{title.split()[0]} Frame'),
                ('lock', 'Lock'),
                ('hinge', 'Hinge')
            ]
        else:  # doors
            # TODO: Define door file types (4 files)
            file_types = [
                ('door', f'{title.split()[0]} Door'),
                ('lock', 'Lock'),
                ('hinge', 'Hinge'),
                ('other', 'Other')  # Placeholder
            ]
        
        # Create file item placeholders
        for file_type, display_name in file_types:
            # TODO: Create GeneratedFileItem widgets
            item_label = ThemedLabel(f"{display_name}: [File Item Placeholder]")
            item_label.setStyleSheet("QLabel { padding: 5px; border: 1px solid #444; margin: 2px; }")
            group_layout.addWidget(item_label)
            
            # Store reference
            self.file_items[side][file_type] = item_label
        
        # Add stretch
        group_layout.addStretch()
        
        return widget
    
    def connect_signals(self):
        """Connect widget signals"""
        self.generate_button.clicked.connect(self.generate_files)
    
    def showEvent(self, event):
        """Handle tab being shown - generate files only on first time"""
        super().showEvent(event)
        
        if self.first_time_opened:
            self.first_time_opened = False
            self.generate_files()
    
    def generate_files(self):
        """Generate files - only when explicitly called"""
        # TODO: Implement file generation logic
        # This should:
        # 1. Process gcodes with current parameters
        # 2. Copy processed to generated
        # 3. Update file item widgets
        print(f"Generate files called for context: {self.context}")
    
    def export_files(self):
        """Export all files to the output directory with proper cnc structure"""
        try:
            # Ensure output directory exists
            os.makedirs(self.output_dir, exist_ok=True)
            
            # Remove existing cnc directory if it exists
            cnc_dir = os.path.join(self.output_dir, "cnc")
            if os.path.exists(cnc_dir):
                shutil.rmtree(cnc_dir)
            
            # Create new cnc directory structure
            os.makedirs(cnc_dir, exist_ok=True)
            
            exported_files = []
            
            for side_en, side_fr in [('left', 'gauche'), ('right', 'droite')]:
                side_dir = os.path.join(cnc_dir, side_fr)
                os.makedirs(side_dir, exist_ok=True)
                
                # Export files for this side
                for file_type in self.file_items[side_en].keys():
                    # TODO: Get actual content from file items
                    content = f"Generated G-code for {side_en} {file_type}"
                    
                    # Convert line endings to Windows format
                    content_windows = content.replace('\n', '\r\n').replace('\r\r\n', '\r\n')
                    
                    filename = f"{side_en}_{file_type}.txt"
                    filepath = os.path.join(side_dir, filename)
                    
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content_windows)
                    
                    exported_files.append(filepath)
            
            # Show success message
            file_count = len(exported_files)
            QMessageBox.information(self, "Export Successful",
                                  f"Exported {file_count} files to:\n{cnc_dir}")
        
        except Exception as e:
            QMessageBox.critical(self, "Export Failed",
                               f"Failed to export files:\n{str(e)}")
    
    def browse_output_dir(self):
        """Browse for output directory"""
        dir_path = QFileDialog.getExistingDirectory(
            self, "Select Output Directory", self.output_dir
        )
        if dir_path:
            self.output_dir = dir_path
            self.output_path.setText(dir_path)
    
    def check_and_update_sync_status(self):
        """Check if generated gcodes match processed gcodes and update highlighting"""
        # TODO: Implement sync status checking
        pass
    
    def update_file_items_from_manager(self):
        """Update file items with content from project manager"""
        # TODO: Implement file item updates from manager
        pass
