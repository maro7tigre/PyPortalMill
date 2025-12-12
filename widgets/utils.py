from PySide6.QtGui import QPixmap, QColor, QPainter
from PySide6.QtCore import Qt

class PlaceholderPixmap:
    """Utility class for creating placeholder pixmaps with text/icons"""
    
    @staticmethod
    def create(size, text="", background_color="#44475c", text_color="#bdbdc0"):
        """Create a placeholder pixmap with text"""
        pixmap = QPixmap(*size)
        pixmap.fill(QColor(background_color))
        
        if text:
            painter = QPainter(pixmap)
            painter.setPen(QColor(text_color))
            painter.drawText(pixmap.rect(), Qt.AlignCenter, text)
            painter.end()
        
        return pixmap
    
    @staticmethod
    def create_profile_placeholder(size=(150, 150)):
        """Create profile image placeholder"""
        return PlaceholderPixmap.create(size, "Profile Image")
    
    @staticmethod
    def create_type_placeholder(size=(80, 80)):
        """Create type image placeholder"""
        return PlaceholderPixmap.create(size, "📐")
    
    @staticmethod
    def create_add_button(size=(80, 80)):
        """Create add button placeholder"""
        return PlaceholderPixmap.create(size, "+")
    
    @staticmethod
    def create_file_icon(size=(60, 60), icon="📄"):
        """Create file icon placeholder"""
        return PlaceholderPixmap.create(size, icon)
