import json
import os
import shutil
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any, Optional
from PySide6.QtCore import QObject, Signal

@dataclass
class ProfileConfig:
    id: str
    name: str
    type: str # "hardware", etc.
    shared_with: List[str] = field(default_factory=list)
    # Validation rules
    is_required: bool = False

@dataclass
class ParameterConfig:
    name: str
    label: str
    type: str # "float", "int", "string", "enum", "bool"
    default: Any
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    options: List[str] = field(default_factory=list)
    has_auto: bool = False

@dataclass
class GroupedAutoConfig:
    enabled: bool
    label: str
    controlled_params: List[str]
    default_active: bool

@dataclass
class ParameterSectionConfig:
    id: str
    title: str
    position: str # "left", "right"
    parameters: List[ParameterConfig]
    grouped_auto: Optional[GroupedAutoConfig] = None

@dataclass
class PreviewShapeConfig:
    id: str
    type: str  # "rectangle", "circle"
    x: Any  # str (equation) or float
    y: Any  # str (equation) or float
    width: Any  # str (equation) or float
    height: Any  # str (equation) or float
    color: str  # Hex string like "#RRGGBB"
    border_color: str = "#000000"
    border_width: int = 1

@dataclass
class TabConfig:
    id: str
    name: str
    profiles: List[ProfileConfig]
    parameter_sections: List[ParameterSectionConfig]
    # Validation rule for profiles: "none", "require_one", "require_all"
    profile_validation: str = "none"
    preview: List[PreviewShapeConfig] = field(default_factory=list)

class ConfigManager(QObject):
    """
    Singleton-like manager for application configuration.
    Supports default (read-only) and user (read-write) configurations.
    """
    _instance = None
    
    # Signal emitted when configuration changes
    config_changed = Signal(str) # config_name

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
            cls._instance.initialized = False
        return cls._instance
    
    def __init__(self):
        # Prevent re-initialization
        if getattr(self, 'initialized', False):
            return
            
        super().__init__()
        self.initialized = True
        
        # Paths
        self.root_dir = Path(os.getcwd())
        self.config_dir = self.root_dir / "config"
        self.user_config_dir = self.config_dir / "user_configs"
        self.user_config_dir.mkdir(exist_ok=True)
        
        self.default_config_path = self.config_dir / "settings.json"
        
        # Data storage
        self.configs: Dict[str, Dict] = {} # raw json data
        self.tabs: List[TabConfig] = []
        self.current_config_name = "Default"
        
        # Load all configs
        self.reload_configs()

    def reload_configs(self):
        """Reload all configurations from disk"""
        self.configs = {}
        
        # Load Default
        if self.default_config_path.exists():
            try:
                with open(self.default_config_path, 'r', encoding='utf-8') as f:
                    self.configs["Default"] = json.load(f)
            except Exception as e:
                print(f"Error loading default config: {e}")
        
        # Load User Configs
        if self.user_config_dir.exists():
            for config_file in self.user_config_dir.glob("*.json"):
                try:
                    with open(config_file, 'r', encoding='utf-8') as f:
                        name = config_file.stem
                        self.configs[name] = json.load(f)
                except Exception as e:
                    print(f"Error loading user config {config_file}: {e}")
        
        # Ensure we have a current config loaded into objects
        if self.current_config_name not in self.configs:
            self.current_config_name = "Default"
            
        self._parse_current_config()

    def _parse_current_config(self):
        """Parse the currently active configuration into objects"""
        data = self.configs.get(self.current_config_name, {})
        self.tabs = []
        
        if not data:
            return

        for tab_data in data.get("tabs", []):
            
            # Parse Profiles
            profiles = []
            for p in tab_data.get("profiles", []):
                profiles.append(ProfileConfig(
                    id=p.get("id"),
                    name=p.get("name"),
                    type=p.get("type", "hardware"),
                    shared_with=p.get("shared_with", []),
                    is_required=p.get("is_required", False)
                ))
            
            # Parse Parameter Sections
            sections = []
            for s in tab_data.get("parameter_sections", []):
                
                # Parse Parameters
                params = []
                for p in s.get("parameters", []):
                    params.append(ParameterConfig(
                        name=p.get("name"),
                        label=p.get("label"),
                        type=p.get("type", "string"),
                        default=p.get("default"),
                        min_value=p.get("min"),
                        max_value=p.get("max"),
                        options=p.get("options", []),
                        has_auto=p.get("has_auto", False)
                    ))
                
                # Parse Grouped Auto
                grouped_auto = None
                ga_data = s.get("grouped_auto")
                if ga_data:
                    grouped_auto = GroupedAutoConfig(
                        enabled=ga_data.get("enabled", False),
                        label=ga_data.get("label", "Auto"),
                        controlled_params=ga_data.get("controlled_params", []),
                        default_active=ga_data.get("default_active", False)
                    )
                
                sections.append(ParameterSectionConfig(
                    id=s.get("id"),
                    title=s.get("title", ""),
                    position=s.get("position", "left"),
                    parameters=params,
                    grouped_auto=grouped_auto
                ))
            
            # Parse Preview Shapes
            preview_shapes = []
            for shape in tab_data.get("preview", []):
                preview_shapes.append(PreviewShapeConfig(
                    id=shape.get("id", f"shape_{len(preview_shapes)}"),
                    type=shape.get("type", "rectangle"),
                    x=shape.get("x", 0.0),
                    y=shape.get("y", 0.0),
                    width=shape.get("width", 50.0),
                    height=shape.get("height", 50.0),
                    color=shape.get("color", "#CCCCCC"),
                    border_color=shape.get("border_color", "#000000"),
                    border_width=shape.get("border_width", 1)
                ))

            self.tabs.append(TabConfig(
                id=tab_data.get("id"),
                name=tab_data.get("name"),
                profiles=profiles,
                parameter_sections=sections,
                profile_validation=tab_data.get("profile_validation", "none"),
                preview=preview_shapes
            ))

    def get_tabs(self) -> List[TabConfig]:
        return self.tabs
        
    def get_tab_by_id(self, tab_id: str) -> Optional[TabConfig]:
        for tab in self.tabs:
            if tab.id == tab_id:
                return tab
        return None

    def get_available_configs(self) -> List[str]:
        """Get list of available configuration names"""
        return list(self.configs.keys())

    def set_config(self, config_name: str) -> bool:
        """Switch active configuration"""
        if config_name not in self.configs:
            return False
            
        self.current_config_name = config_name
        self._parse_current_config()
        self.config_changed.emit(config_name)
        return True

    def get_config_data(self, config_name: str) -> Optional[Dict]:
        """Get raw config data"""
        return self.configs.get(config_name)

    def save_user_config(self, name: str, data: Dict) -> bool:
        """Save a new or existing user configuration"""
        if name == "Default":
            print("Cannot overwrite Default config")
            return False
            
        try:
            file_path = self.user_config_dir / f"{name}.json"
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            
            self.configs[name] = data
            
            # If we just saved the current config, re-parse it to ensure consistency
            if self.current_config_name == name:
                self._parse_current_config()
                self.config_changed.emit(name)
                
            return True
        except Exception as e:
            print(f"Error saving config {name}: {e}")
            return False

    def delete_user_config(self, name: str) -> bool:
        """Delete a user configuration"""
        if name == "Default":
            return False
            
        if name not in self.configs:
            return False
            
        try:
            file_path = self.user_config_dir / f"{name}.json"
            if file_path.exists():
                file_path.unlink()
            
            del self.configs[name]
            
            # If we deleted the current config, revert to Default
            if self.current_config_name == name:
                self.set_config("Default")
                
            return True
        except Exception as e:
            print(f"Error deleting config {name}: {e}")
            return False

# Global Accessor
def get_config_manager():
    return ConfigManager()
