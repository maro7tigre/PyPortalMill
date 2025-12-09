"""
PyPortalMill - Main Application Entry Point
"""

import sys
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow


def main():
    """Main application entry point"""
    app = QApplication(sys.argv)
    
    # Set application metadata
    app.setApplicationName("PyPortalMill")
    app.setOrganizationName("PyPortalMill")
    app.setStyle("Fusion")
    
    # Initialize Coordinator
    # (Lazy import to avoid circular dependencies if any, though likely fine here)
    from core.app_coordinator import AppCoordinator
    
    coordinator = AppCoordinator(app)
    coordinator.start()
    
    # Start event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
