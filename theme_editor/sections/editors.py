"""
Editors Section
GCode and syntax highlighting.
"""

from PySide6.QtWidgets import QLabel
from ..base_section import ThemeEditorSection
from widgets.editors.gcode import GCodeEditor

class EditorsSection(ThemeEditorSection):
    def setup_config_ui(self):
        self.add_header("Syntax Highlighting")
        
        colors = [
            ('variable', 'Variables', '#ff8c00'),
            ('g0', 'G0 (Rapid)', '#d15e43'),
            ('g1', 'G1 (Linear)', '#286c34'),
            ('gm', 'Other G/M', '#5e9955'),
            ('x', 'X Axis', '#c8b723'),
            ('y', 'Y Axis', '#009ccb'),
            ('z', 'Z Axis', '#ff4a7c'),
            ('line', 'Line Numbers', '#8A817C'),
            ('comment', 'Comments', '#B0B8B4')
        ]
        
        for key, label, default in colors:
            self.add_color_control(label, f'syntax.{key}', default)

    def setup_preview_ui(self):
        layout = self.preview_inner_layout
        
        editor = GCodeEditor()
        editor.setPlainText("; Sample G-Code\nG0 X0 Y0 Z10\nG1 X100 Y50 F1000\n#VAR = 100")
        editor.setFixedHeight(200)
        
        layout.addWidget(QLabel("G-Code Editor Preview"))
        layout.addWidget(editor)
        layout.addStretch()
