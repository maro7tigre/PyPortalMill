"""
Data Models for PyPortalMill
Defines the structure for Hardware, Profiles, and Project configurations.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any


@dataclass
class HardwareVariable:
    """Represents a variable definition in a hardware type"""
    name: str
    default_value: str
    description: str = ""


@dataclass
class HardwareType:
    """
    Defines the capabilities and G-code generation logic for a specific hardware category
    (e.g., "Standard Hinge" or "European Lock")
    """
    name: str
    gcode_template: str
    image_path: str = ""
    preview_path: str = ""
    # Stores variables as a list of [name, default] lists, matching legacy format, 
    # or we can process them into a cleaner dict. Sticking to a structured approach:
    variables: List[List[str]] = field(default_factory=list) 

    @property
    def variable_dict(self) -> Dict[str, str]:
        """Returns variables as a dictionary for easier access"""
        return {v[0]: v[1] for v in self.variables if len(v) >= 2}


@dataclass
class HardwareProfile:
    """
    A user-configured instance of a HardwareType.
    (e.g., "Chwari German Hinge" which uses "Standard Hinge" logic but with specific dims)
    """
    name: str
    type_name: str  # References a HardwareType.name
    l_variables: Dict[str, str] = field(default_factory=dict)
    custom_variables: Dict[str, str] = field(default_factory=dict)
    image_path: str = ""


@dataclass
class FrameConfig:
    """Configuration for frame G-code generation"""
    right_gcode: str = ""
    left_gcode: str = ""


@dataclass
class ParameterDefinition:
    """Defines a single parameter for doors or frames"""
    name: str
    display_name: str
    param_type: str  # "float", "int", "string", "enum", "bool"
    default_value: Any
    category: str = "General"  # For grouping in UI
    has_auto: bool = False  # Supports auto-calculation
    image_path: str = ""  # Preview image for this parameter
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    enum_values: List[str] = field(default_factory=list)  # For enum types


@dataclass
class DoorsParameterSet:
    """Parameter set for doors"""
    parameters: Dict[str, ParameterDefinition] = field(default_factory=dict)


@dataclass
class FramesParameterSet:
    """Parameter set for frames (similar to old system)"""
    parameters: Dict[str, ParameterDefinition] = field(default_factory=dict)


@dataclass
class ProjectData:
    """
    The Root Data Object matching the new dynamic configuration structure.
    """
    # Hardware Types definitions (loaded from disk/config, but maybe stored here for portability)
    # Key = type_id (e.g., "hinge", "lock")
    hardware_types: Dict[str, Dict[str, HardwareType]] = field(default_factory=dict)
    
    # User-configured Profiles
    # Key = type_id (e.g., "hinge", "lock") -> Profile Name -> HardwareProfile
    hardware_profiles: Dict[str, Dict[str, HardwareProfile]] = field(default_factory=dict)
    
    # Global/Tab settings
    # Key = tab_id (e.g. "doors", "frames") -> config object
    tab_configurations: Dict[str, Any] = field(default_factory=dict)
    
    # Parameter values for each context
    # Key = context_id (e.g., "doors", "frames") -> param_name -> value
    parameter_values: Dict[str, Dict[str, Any]] = field(default_factory=dict)

