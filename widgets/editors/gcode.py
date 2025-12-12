"""
G-Code Editor Module

Complete G-code editor with syntax highlighting, line numbers, 
error indication, and $ variables support.
"""

from PySide6.QtWidgets import (QPlainTextEdit, QWidget, QTextEdit, QToolTip, QPushButton)
from PySide6.QtGui import (QColor, QFont, QSyntaxHighlighter, QTextCursor, QPainter, 
                         QPalette, QTextCharFormat, QTextFormat)
from PySide6.QtCore import QSize, Qt, QRect, Signal, QTimer
import re
from core.theme_manager import get_theme_manager
from widgets import ThemedWidgetMixin


class GCodeSyntaxHighlighter(QSyntaxHighlighter):
    """Enhanced G-code syntax highlighter with $ variable validation"""
    
    def __init__(self, document, dollar_variables_info=None):
        super().__init__(document)
        self.dollar_variables_info = dollar_variables_info or {}
        
        self.font = QFont('Consolas', 18)
        self.font.setFixedPitch(True)
        
        # Initialize formats with default colors (will be updated via update_colors)
        self.formats = {}
        self.update_colors()
        
    def update_colors(self):
        """Update syntax colors from ThemeManager"""
        tm = get_theme_manager()
        
        def create_format(color_key, default_color, bg_key=None, bg_default=None):
            fmt = QTextCharFormat()
            # Fetch from syntax section, fallback to default
            color_str = tm.get_color(f'syntax.{color_key}')
            if not color_str: # fallback if key missing
                 color_str = default_color
            
            color = QColor(color_str) 
            fmt.setForeground(color)
            
            if bg_key:
                bg_str = tm.get_color(f'syntax.{bg_key}')
                if not bg_str:
                    bg_str = bg_default
                fmt.setBackground(QColor(bg_str))
                
            fmt.setFont(self.font)
            return fmt

        self.variable_format = create_format('variable', '#ff8c00') # Orange -> Accents.warning
        self.valid_dollar_format = create_format('dollar_valid', '#23c87b') # Green -> Accents.secondary
        self.invalid_dollar_format = create_format('dollar_invalid', '#ff4a7c', 'dollar_invalid_bg', '#2d1f1f') # Red -> Accents.error
        
        self.g0_format = create_format('g0', '#d15e43')
        self.g1_format = create_format('g1', '#286c34')
        self.gm_format = create_format('gm', '#5e9955')
        self.x_format = create_format('x', '#c8b723')
        self.y_format = create_format('y', '#009ccb') # Blue -> Text.links
        self.z_format = create_format('z', '#ff4a7c')
        self.r_format = create_format('r', '#6320a1')
        self.i_format = create_format('i', '#dc2626')
        self.j_format = create_format('j', '#059669')
        self.fs_format = create_format('fs', '#e66c00')
        self.line_format = create_format('line', '#8A817C') # Gray -> Text.disabled
        self.l_var_format = create_format('l_var', '#BB86FC') # Purple -> Accents.primary
        self.comment_format = create_format('comment', '#B0B8B4') # Text.secondary
        

    
    def update_dollar_variables(self, dollar_variables_info):
        """Update available $ variables for validation"""
        self.dollar_variables_info = dollar_variables_info
        self.rehighlight()

    def highlightBlock(self, text):
        """Apply syntax highlighting using character-by-character parsing"""
        i = 0
        length = len(text)
        
        while i < length:
            # Skip whitespace
            if text[i].isspace():
                i += 1
                continue
            
            # Handle comments - everything after semicolon
            if text[i] == ';':
                self.setFormat(i, length - i, self.comment_format)
                break
            
            # Handle variables {anything} including $ variables
            if text[i] == '{':
                start = i
                i += 1
                var_content = ""
                while i < length and text[i] != '}':
                    var_content += text[i]
                    i += 1
                if i < length:  # Found closing }
                    i += 1
                    # Determine variable type and format
                    var_name = var_content.split(':')[0]  # Remove default value part
                    
                    if var_name.startswith('$'):
                        # $ variable - check if valid
                        dollar_var = var_name[1:]  # Remove $ prefix
                        if dollar_var in self.dollar_variables_info:
                            self.setFormat(start, i - start, self.valid_dollar_format)
                        else:
                            self.setFormat(start, i - start, self.invalid_dollar_format)
                    else:
                        # Regular variable
                        self.setFormat(start, i - start, self.variable_format)
                continue
            
            # Handle letters followed by values
            if text[i].isalpha():
                letter_start = i
                letter = text[i].upper()
                i += 1
                
                # Skip any whitespace after letter
                while i < length and text[i].isspace():
                    i += 1
                
                # Different parsing for L vs other letters
                if letter == 'L':
                    # L variables only have numbers (L1, L24, L245)
                    value_start = i
                    while i < length and text[i].isdigit():
                        i += 1
                    
                    # Only highlight if there are digits after L
                    if i > value_start:
                        self.setFormat(letter_start, i - letter_start, self.l_var_format)
                else:
                    # Other letters can have complex values (numbers, +, -, *, /, L, variables)
                    value_start = i
                    while i < length and (text[i].isdigit() or text[i] in '+-*/.L' or 
                                         (text[i] == '{' and self._find_closing_brace(text, i) != -1)):
                        if text[i] == '{':
                            # Skip entire variable
                            close_pos = self._find_closing_brace(text, i)
                            if close_pos != -1:
                                i = close_pos + 1
                            else:
                                i += 1
                        else:
                            i += 1
                    
                    # Apply formatting based on letter (only if there's a value)
                    total_length = i - letter_start
                    if total_length > 1:
                        if letter == 'G':
                            # Check for specific G codes
                            value_text = text[value_start:i].strip()
                            if value_text in ['0', '00']:
                                self.setFormat(letter_start, total_length, self.g0_format)
                            elif value_text in ['1', '01']:
                                self.setFormat(letter_start, total_length, self.g1_format)
                            else:
                                self.setFormat(letter_start, total_length, self.gm_format)
                        elif letter == 'M':
                            self.setFormat(letter_start, total_length, self.gm_format)
                        elif letter == 'X':
                            self.setFormat(letter_start, total_length, self.x_format)
                        elif letter == 'Y':
                            self.setFormat(letter_start, total_length, self.y_format)
                        elif letter == 'Z':
                            self.setFormat(letter_start, total_length, self.z_format)
                        elif letter == 'R':
                            self.setFormat(letter_start, total_length, self.r_format)
                        elif letter == 'I':
                            self.setFormat(letter_start, total_length, self.i_format)
                        elif letter == 'J':
                            self.setFormat(letter_start, total_length, self.j_format)
                        elif letter in ['F', 'S']:
                            self.setFormat(letter_start, total_length, self.fs_format)
                        elif letter == 'N':
                            self.setFormat(letter_start, total_length, self.line_format)
                continue
            
            # Skip any other character
            i += 1
    
    def _find_closing_brace(self, text, start):
        """Find the closing brace for a variable starting at position start"""
        i = start + 1
        while i < len(text):
            if text[i] == '}':
                return i
            i += 1
        return -1


class LineNumberArea(QWidget):
    """Line number area with error indication"""
    
    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor  # Reference to the GCodeEditor
        self.setMouseTracking(True)
        self.clickedLineNumber = None

    def sizeHint(self):
        return QSize(self.editor.lineNumberAreaWidth(), 0)

    def paintEvent(self, event):
        self.editor.lineNumberAreaPaintEvent(event)
        
    def mousePressEvent(self, event):
        """Handle error tooltip display"""
        if event.button() == Qt.LeftButton:
            block = self.editor.firstVisibleBlock()
            blockNumber = block.blockNumber()
            top = self.editor.blockBoundingGeometry(block).translated(self.editor.contentOffset()).top()
            bottom = top + self.editor.blockBoundingRect(block).height()

            while block.isValid() and top <= event.pos().y():
                if block.isVisible() and bottom >= event.pos().y():
                    lineNumber = blockNumber + 1
                    if lineNumber in self.editor.errors:
                        if self.clickedLineNumber == lineNumber:
                            self.clickedLineNumber = None
                            QToolTip.hideText()
                        else:
                            self.clickedLineNumber = lineNumber
                            errors = self.editor.errors[lineNumber]
                            tooltip_text = "\\n".join([f"- {trigger} : {message}" for message, trigger, _ in errors])
                            QToolTip.showText(event.globalPos(), tooltip_text, self)
                    else:
                        self.clickedLineNumber = None
                        QToolTip.hideText()
                    break

                block = block.next()
                top = bottom
                bottom = top + self.editor.blockBoundingRect(block).height()
                blockNumber += 1


class GCodeEditor(QPlainTextEdit, ThemedWidgetMixin):
    """G-code editor with smart highlighting, $ variable support, and help dialog"""
    
    variables_changed = Signal(list)
    show_help_requested = Signal()  # Request help dialog from parent
    
    def __init__(self, parent=None):
        super().__init__(parent)
        ThemedWidgetMixin.__init__(self)
        self.module = parent
        self.lineNumberArea = LineNumberArea(self)
        self.errors = {}
        self.variables = []
        self.selected_text = ""
        self.selection_timer = QTimer()
        self.selection_timer.setSingleShot(True)
        self.selection_timer.timeout.connect(self.highlightSelections)
        self.dollar_variables_info = {}

        # Setup appearance
        # Setup appearance
        self.update_style()
        
        self.setFont(QFont('Consolas', 18))
        self.setLineWrapMode(QPlainTextEdit.NoWrap)

        # Setup highlighter
        self.highlighter = GCodeSyntaxHighlighter(self.document(), self.dollar_variables_info)

        # Connect signals
        self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.updateRequest.connect(self.updateLineNumberArea)
        self.cursorPositionChanged.connect(self.onCursorPositionChanged)
        self.textChanged.connect(self.onTextChanged)
        self.selectionChanged.connect(self.onSelectionChanged)
        
        self.updateLineNumberAreaWidth(0)
        
        # Create help button
        self.create_help_button()

    def create_help_button(self):
        """Create the ? button for showing $ variables"""
        self.help_button = QPushButton("?", self)
        self.help_button.setFixedSize(25, 25)
        self.help_button.setStyleSheet("""
            QPushButton {
                background-color: #BB86FC;
                color: #1d1f28;
                border: none;
                border-radius: 12px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #9965DA;
            }
            QPushButton:pressed {
                background-color: #7c4dff;
            }
        """)
        self.help_button.clicked.connect(self.show_dollar_variables_help)
        self.help_button.setToolTip("Show available $ variables")
        
        # Position button in top-right corner
        self.position_help_button()
    
    def position_help_button(self):
        """Position the help button in the top-right corner"""
        margin = 10
        self.help_button.move(
            self.viewport().width() - self.help_button.width() - margin,
            margin
        )
    
    def resizeEvent(self, event):
        """Handle resize to reposition help button and line numbers"""
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(QRect(cr.left(), cr.top(), self.lineNumberAreaWidth(), cr.height()))
        self.position_help_button()
    
    def set_dollar_variables_info(self, variables_info):
        """Set available $ variables information"""
        self.dollar_variables_info = variables_info
        self.highlighter.update_dollar_variables(variables_info)
    
    def show_dollar_variables_help(self):
        """Request help dialog with available $ variables"""
        self.show_help_requested.emit()
    
    def insert_variable(self, variable_text):
        """Insert a variable at current cursor position"""
        cursor = self.textCursor()
        cursor.insertText(variable_text)

    # Line Numbers
    def lineNumberAreaWidth(self):
        """Calculate line number area width"""
        digits = 1
        max_num = max(1, self.blockCount())
        while max_num >= 10:
            max_num /= 10
            digits += 1
        return 3 + self.fontMetrics().boundingRect('9').width() * digits

    def updateLineNumberAreaWidth(self, _):
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)

    def updateLineNumberArea(self, rect, dy):
        if dy:
            self.lineNumberArea.scroll(0, dy)
        else:
            self.lineNumberArea.update(0, rect.y(), self.lineNumberArea.width(), rect.height())
        if rect.contains(self.viewport().rect()):
            self.updateLineNumberAreaWidth(0)

    def lineNumberAreaPaintEvent(self, event):
        """Paint line numbers"""
        painter = QPainter(self.lineNumberArea)
        
        block = self.firstVisibleBlock()
        blockNumber = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(blockNumber + 1)
                if (blockNumber + 1) in self.errors:
                    painter.fillRect(0, top, self.lineNumberArea.width(), bottom - top, QColor('#ff4a7c'))
                    painter.setPen(QColor('#1d1f28'))
                else:
                    painter.fillRect(0, top, self.lineNumberArea.width(), bottom - top, QColor('#1d1f28'))
                    painter.setPen(QColor('#8b95c0'))
                    
                painter.drawText(0, top, self.lineNumberArea.width() - 2, self.fontMetrics().height(), Qt.AlignRight, number)
                
            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            blockNumber += 1

    # Highlighting
    def onCursorPositionChanged(self):
        self.highlightCurrentLine()
        if hasattr(self.module, 'updatePreviewColors'):
            self.module.updatePreviewColors()

    def highlightCurrentLine(self):
        """Highlight current line"""
        extraSelections = []
        if not self.isReadOnly():
            lineColor = QColor('#00c4fe')
            lineColor.setAlpha(15)
            
            cursor = self.textCursor()
            if cursor.hasSelection():
                start = cursor.selectionStart()
                end = cursor.selectionEnd()
                block = self.document().findBlock(start)
                while block.isValid() and block.position() <= end:
                    selection = QTextEdit.ExtraSelection()
                    selection.format.setBackground(lineColor)
                    selection.format.setProperty(QTextFormat.FullWidthSelection, True)
                    selection.cursor = QTextCursor(block)
                    extraSelections.append(selection)
                    block = block.next()
            else:
                selection = QTextEdit.ExtraSelection()
                selection.format.setBackground(lineColor)
                selection.format.setProperty(QTextFormat.FullWidthSelection, True)
                selection.cursor = cursor
                selection.cursor.clearSelection()
                extraSelections.append(selection)
        
        self.setExtraSelections(extraSelections)

    def onSelectionChanged(self):
        """Handle selection changes for highlighting occurrences"""
        cursor = self.textCursor()
        if cursor.hasSelection():
            selected = cursor.selectedText().strip()
            if len(selected) > 1 and selected != self.selected_text:
                self.selected_text = selected
                self.selection_timer.start(300)
        else:
            self.selected_text = ""
            self.highlightCurrentLine()

    def highlightSelections(self):
        """Highlight all occurrences of selected text"""
        if not self.selected_text:
            self.highlightCurrentLine()
            return

        extraSelections = []
        
        # Current line
        lineColor = QColor('#00c4fe')
        lineColor.setAlpha(15)
        cursor = self.textCursor()
        if not cursor.hasSelection():
            selection = QTextEdit.ExtraSelection()
            selection.format.setBackground(lineColor)
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            selection.cursor = cursor
            selection.cursor.clearSelection()
            extraSelections.append(selection)

        # All occurrences
        selectionColor = QColor('#1e3a8a')
        selectionColor.setAlpha(120)
        
        document = self.document()
        cursor = QTextCursor(document)
        
        while True:
            cursor = document.find(self.selected_text, cursor)
            if cursor.isNull():
                break
            selection = QTextEdit.ExtraSelection()
            selection.format.setBackground(selectionColor)
            selection.cursor = cursor
            extraSelections.append(selection)

        self.setExtraSelections(extraSelections)

    def getHighlightedLines(self):
        """Get highlighted line numbers"""
        cursor = self.textCursor()
        if cursor.hasSelection():
            start = cursor.selectionStart()
            end = cursor.selectionEnd()
            startBlock = self.document().findBlock(start)
            endBlock = self.document().findBlock(end)
            startLineNumber = startBlock.blockNumber() + 1
            endLineNumber = endBlock.blockNumber() + 1
            return list(range(startLineNumber, endLineNumber + 1))
        else:
            return [cursor.blockNumber() + 1]

    # Variables
    def onTextChanged(self):
        """Extract variables from text"""
        text = self.toPlainText()
        pattern = r'\{([A-Z]\d+)(?::([0-9.]+))?\}'
        matches = re.findall(pattern, text)
        
        new_variables = []
        seen = set()
        for var_name, default in matches:
            if var_name not in seen:
                new_variables.append((var_name, default))
                seen.add(var_name)
        
        new_variables.sort(key=lambda x: x[0])
        
        if new_variables != self.variables:
            self.variables = new_variables
            self.variables_changed.emit(self.variables)

    def getVariables(self):
        return self.variables.copy()

    def insertVariable(self, variable_name, default_value=None):
        cursor = self.textCursor()
        if default_value:
            cursor.insertText(f"{{{variable_name}:{default_value}}}")
        else:
            cursor.insertText(f"{{{variable_name}}}")

    # Utilities
    def setErrors(self, errors):
        self.errors = errors
        self.lineNumberArea.update()

    def focusOutEvent(self, event):
        super().focusOutEvent(event)
        if hasattr(self.lineNumberArea, 'clickedLineNumber'):
            self.lineNumberArea.clickedLineNumber = None
            QToolTip.hideText()

    def on_theme_changed(self, theme_name):
        """Handle theme updates"""
        try:
            self.update_style()
            if hasattr(self, 'highlighter'):
                self.highlighter.update_colors()
                self.highlighter.rehighlight()
        except RuntimeError:
            # Widget might be deleted but signal still firing
            pass
            
    def update_style(self):
        """Apply theme colors"""
        tm = get_theme_manager()
        palette = self.palette()
        palette.setColor(QPalette.Base, QColor(tm.get_color("backgrounds.input")))
        palette.setColor(QPalette.Text, QColor(tm.get_color("text.primary")))
        self.setPalette(palette)
        
        # Update help button style if needed
        # (It uses static style currently, could be dynamic)
