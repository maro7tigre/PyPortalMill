"""
App Coordinator
Orchestrates the application flow, initializes the ProjectManager, and manages the Main Window.
"""

import os
from typing import Optional

from PySide6.QtWidgets import QApplication

from core.project_manager import ProjectManager
from core.parameter_manager import ParameterManager
from ui.main_window import MainWindow


class AppCoordinator:
    """
    Main controller for the application.
    """
    def __init__(self, app: QApplication):
        self.app = app
        self.root_dir = os.getcwd()
        
        # Initialize Core Pillars
        self.project_manager = ProjectManager(self.root_dir)
        self.parameter_manager = ParameterManager()  # NEW: Parameter management
        
        # Initialize UI (start with None)
        self.main_window: Optional[MainWindow] = None

    def start(self):
        """Starts the application"""
        print("AppCoordinator: Starting application...")
        
        # 1. Load Data
        self._connect_signals()
        self.project_manager.load_data()
        
        # 2. Launch UI
        self.main_window = MainWindow()
        # In a real MVVM-C, we would inject the coordinator or viewmodels here
        # self.main_window.set_coordinator(self) 
        
        self.main_window.show()
        print("AppCoordinator: UI Launched.")

    def _connect_signals(self):
        """Connects core signals (logging, errors)"""
        self.project_manager.data_loaded.connect(self._on_data_loaded)
        self.project_manager.error_occurred.connect(self._on_error)

    def _on_data_loaded(self):
        print("AppCoordinator: Project data loaded successfully.")
        # Here we would verify data or trigger UI updates

    def _on_error(self, message: str):
        print(f"AppCoordinator Error: {message}")
        # Here we could show a QMessageBox if the UI is ready
