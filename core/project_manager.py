"""
Project Manager
Handles loading and saving of project data (profiles, hardware types).
Acts as the Central Model for the application.
"""

import json
import os
from pathlib import Path
from typing import Optional

from PySide6.QtCore import QObject, Signal

from core.models import (
    ProjectData, HardwareType, HardwareProfile, FrameConfig
)


class ProjectManager(QObject):
    """
    Singleton-like class that manages the application state and data persistence.
    """
    
    # Signals
    data_loaded = Signal()
    error_occurred = Signal(str)

    def __init__(self, root_dir: str):
        super().__init__()
        self.root_dir = Path(root_dir)
        self.profiles_dir = self.root_dir / "profiles"
        self.current_project_file = self.profiles_dir / "current.json"
        
        # In-memory data
        self.project_data: Optional[ProjectData] = None

    def load_data(self):
        """Loads the project data from current.json"""
        if not self.current_project_file.exists():
            self.error_occurred.emit(f"Profile file not found: {self.current_project_file}")
            return

        try:
            with open(self.current_project_file, 'r') as f:
                raw_data = json.load(f)
            
            self.project_data = self._parse_project_data(raw_data)
            self.data_loaded.emit()
            print("Project data loaded successfully.")
            
        except json.JSONDecodeError:
            self.error_occurred.emit("Failed to parse profiles/current.json. Invalid JSON.")
        except Exception as e:
            self.error_occurred.emit(f"Error loading data: {str(e)}")

    def _parse_project_data(self, data: dict) -> ProjectData:
        """Parses raw dictionary into structured ProjectData model"""
        project = ProjectData()
        
        # Parse Hinges
        if "hinges" in data:
            hinges_data = data["hinges"]
            project.hinge_types = self._parse_hardware_types(hinges_data.get("types", {}))
            project.hinge_profiles = self._parse_hardware_profiles(hinges_data.get("profiles", {}))

        # Parse Locks
        if "locks" in data:
            locks_data = data["locks"]
            project.lock_types = self._parse_hardware_types(locks_data.get("types", {}))
            project.lock_profiles = self._parse_hardware_profiles(locks_data.get("profiles", {}))

        # Parse Frame GCode
        if "frame_gcode" in data:
            fg = data["frame_gcode"]
            project.frame_config = FrameConfig(
                right_gcode=fg.get("right_gcode", ""),
                left_gcode=fg.get("left_gcode", "")
            )

        return project

    def _parse_hardware_types(self, types_dict: dict) -> dict:
        """Helper to parse hardware types"""
        parsed = {}
        for key, val in types_dict.items():
            parsed[key] = HardwareType(
                name=val.get("name", key),
                gcode_template=val.get("gcode", ""),
                image_path=val.get("image", ""),
                preview_path=val.get("preview", ""),
                variables=val.get("variables", [])
            )
        return parsed

    def _parse_hardware_profiles(self, profiles_dict: dict) -> dict:
        """Helper to parse hardware profiles"""
        parsed = {}
        for key, val in profiles_dict.items():
            parsed[key] = HardwareProfile(
                name=val.get("name", key),
                type_name=val.get("type", ""),
                l_variables=val.get("l_variables", {}),
                custom_variables=val.get("custom_variables", {}),
                image_path=val.get("image", "")
            )
        return parsed

    def get_hinge_types(self):
        return self.project_data.hinge_types if self.project_data else {}

    def get_hinge_profiles(self):
        return self.project_data.hinge_profiles if self.project_data else {}
    
    def get_lock_types(self):
        return self.project_data.lock_types if self.project_data else {}

    def get_lock_profiles(self):
        return self.project_data.lock_profiles if self.project_data else {}
