"""
Shape Preview Widget
Displays preview shapes defined in the configuration.
Supports parametric rendering using equations and variables.
"""

from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QWidget, QVBoxLayout
from PySide6.QtCore import Qt, QRectF
from PySide6.QtGui import QPen, QBrush, QColor, QPainter
from core.config_manager import PreviewShapeConfig

class ShapePreviewWidget(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        
        # Rendering settings
        self.setRenderHint(QPainter.Antialiasing)
        self.setBackgroundBrush(Qt.NoBrush)
        # Transparent background or let parent decide
        self.setStyleSheet("background: transparent; border: none;")
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        # State
        self.preview_configs: list[PreviewShapeConfig] = []
        self.context_params: dict = {}
        
    def set_data(self, preview_configs, context_params):
        """Update data and redraw"""
        self.preview_configs = preview_configs
        self.context_params = context_params
        self.redraw()
        
    def resizeEvent(self, event):
        """Ensure (0,0) remains in the center when resized"""
        super().resizeEvent(event)
        w = self.viewport().width()
        h = self.viewport().height()
        self.scene.setSceneRect(-w/2, -h/2, w, h)

    def redraw(self):
        self.scene.clear()
        
        # Ensure scene rect is updated if not yet set (e.g. first draw before resize)
        w = self.viewport().width()
        h = self.viewport().height()
        if w > 0 and h > 0:
            self.scene.setSceneRect(-w/2, -h/2, w, h)
        
        # Draw Origin Axes - REMOVED per user request
        # self.scene.addLine(-250, 0, 250, 0, QPen(QColor("#DDDDDD"))) # X Axis
        # self.scene.addLine(0, -250, 0, 250, QPen(QColor("#DDDDDD"))) # Y Axis
        # self.scene.addRect(-250, -250, 500, 500, QPen(Qt.black), QBrush(Qt.NoBrush)) # Border
        
        for shape in self.preview_configs:
            # Resolve properties
            x = self._evaluate_value(shape.x, self.context_params)
            y = self._evaluate_value(shape.y, self.context_params)
            w = self._evaluate_value(shape.width, self.context_params)
            h = self._evaluate_value(shape.height, self.context_params)
            
            fill_color = QColor(shape.color) if QColor.isValidColor(shape.color) else Qt.gray
            border_color = QColor(shape.border_color) if QColor.isValidColor(shape.border_color) else Qt.black
            
            pen = QPen(border_color)
            pen.setWidth(int(shape.border_width))
            brush = QBrush(fill_color)
            
            # X, Y are center of shape
            top_left_x = x - (w / 2)
            top_left_y = y - (h / 2)
            
            if shape.type == "rectangle":
                self.scene.addRect(top_left_x, top_left_y, w, h, pen, brush)
            elif shape.type == "circle":
                self.scene.addEllipse(top_left_x, top_left_y, w, h, pen, brush)

    def _evaluate_value(self, value, context_params):
        """
        Evaluate a value which can be a float, int, or string equation/variable.
        context_params is a dict of {param_name: value}
        """
        if isinstance(value, (int, float)):
            return float(value)
        
        if not isinstance(value, str):
            try:
                return float(value)
            except:
                return 0.0
                
        # String processing
        val_str = value.strip()
        if not val_str:
            return 0.0
            
        # Replace variables "$var" with value
        # Sort params by length desc to avoid partial replacement (e.g. replacing $v in $var)
        sorted_keys = sorted(context_params.keys(), key=len, reverse=True)
        for k in sorted_keys:
            if f"${k}" in val_str:
                val_str = val_str.replace(f"${k}", str(context_params[k]))
                
        # Safe evaluation
        try:
            import math
            allowed_locals = {k: getattr(math, k) for k in dir(math) if not k.startswith('_')}
            return float(eval(val_str, {"__builtins__": None}, allowed_locals))
        except Exception:
            return 0.0
