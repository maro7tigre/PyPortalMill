"""
Parameter Manager
Manages parameters for doors and frames with formula-based linking support (disabled by default)
"""

from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List
from PySide6.QtCore import QObject, Signal


@dataclass
class ParameterLink:
    """Defines a potential formula-based link between two parameters"""
    source_context: str  # "doors" or "frames"
    source_param: str
    target_context: str
    target_param: str
    formula: str = ""  # e.g., "${source} - 10" or "${source} * 0.95"
    enabled: bool = False  # Support for future activation
    bidirectional: bool = False  # Formula links are typically one-way


class ParameterManager(QObject):
    """
    Manages parameters and their potential formula-based links.
    
    Parameters are organized by context (doors/frames) and can be linked
    with formulas for automatic synchronization (when enabled).
    """
    
    # Signals
    parameter_changed = Signal(str, str, object)  # context, param_name, value
    parameters_loaded = Signal(str)  # context
    link_enabled = Signal(str, str, str, str)  # source_context, source_param, target_context, target_param
    
    def __init__(self):
        super().__init__()
        
        # Parameter storage by context
        self.doors_params: Dict[str, Any] = {}
        self.frames_params: Dict[str, Any] = {}
        
        # Link definitions with formulas (disabled by default)
        self.links: List[ParameterLink] = []
    
    def set_parameter(self, context: str, param_name: str, value: Any):
        """
        Set parameter value (with future formula evaluation support).
        
        Args:
            context: "doors" or "frames"
            param_name: Name of the parameter
            value: New value for the parameter
        """
        if context == "doors":
            self.doors_params[param_name] = value
        elif context == "frames":
            self.frames_params[param_name] = value
        else:
            raise ValueError(f"Invalid context: {context}")
        
        # Emit signal
        self.parameter_changed.emit(context, param_name, value)
        
        # Future: Evaluate formulas for enabled links
        # self._evaluate_linked_parameters(context, param_name, value)
    
    def get_parameter(self, context: str, param_name: str, default=None) -> Any:
        """
        Get parameter value.
        
        Args:
            context: "doors" or "frames"
            param_name: Name of the parameter
            default: Default value if parameter doesn't exist
        
        Returns:
            Parameter value or default
        """
        if context == "doors":
            return self.doors_params.get(param_name, default)
        elif context == "frames":
            return self.frames_params.get(param_name, default)
        else:
            raise ValueError(f"Invalid context: {context}")
    
    def get_all_parameters(self, context: str) -> Dict[str, Any]:
        """Get all parameters for a context"""
        if context == "doors":
            return self.doors_params.copy()
        elif context == "frames":
            return self.frames_params.copy()
        else:
            raise ValueError(f"Invalid context: {context}")
    
    def set_parameters_bulk(self, context: str, parameters: Dict[str, Any]):
        """Set multiple parameters at once"""
        if context== "doors":
            self.doors_params.update(parameters)
        elif context == "frames":
            self.frames_params.update(parameters)
        else:
            raise ValueError(f"Invalid context: {context}")
        
        self.parameters_loaded.emit(context)
    
    def define_link(self, link: ParameterLink):
        """
        Define a potential parameter link with formula (disabled by default).
        
        Args:
            link: ParameterLink object defining the link relationship
        """
        # Future: Validate formula syntax
        # self._validate_formula(link.formula)
        
        # Add link definition
        self.links.append(link)
    
    def enable_link(self, source_context: str, source_param: str,
                    target_context: str, target_param: str):
        """
        Enable a defined link (for future use).
        
        Args:
            source_context: Source context ("doors" or "frames")
            source_param: Source parameter name
            target_context: Target context
            target_param: Target parameter name
        """
        for link in self.links:
            if (link.source_context == source_context and
                link.source_param == source_param and
                link.target_context == target_context and
                link.target_param == target_param):
                link.enabled = True
                self.link_enabled.emit(source_context, source_param, 
                                      target_context, target_param)
                return True
        return False
    
    def disable_link(self, source_context: str, source_param: str,
                     target_context: str, target_param: str):
        """Disable a link"""
        for link in self.links:
            if (link.source_context == source_context and
                link.source_param == source_param and
                link.target_context == target_context and
                link.target_param == target_param):
                link.enabled = False
                return True
        return False
    
    def get_links(self, context: Optional[str] = None) -> List[ParameterLink]:
        """
        Get all link definitions, optionally filtered by context.
        
        Args:
            context: Optional filter by source or target context
        
        Returns:
            List of ParameterLink objects
        """
        if context is None:
            return self.links.copy()
        
        return [link for link in self.links 
                if link.source_context == context or link.target_context == context]
    
    def evaluate_formula(self, formula: str, source_value: Any) -> Any:
        """
        Evaluate formula string (for future use).
        
        Formula syntax examples:
        - "${source} - 10" -> source_value - 10
        - "${source} * 0.95" -> source_value * 0.95
        - "${source} / 2" -> source_value / 2
        
        Args:
            formula: Formula string
            source_value: Source parameter value
        
        Returns:
            Evaluated result
        
        Note: This is a placeholder for future formula evaluation.
              When implemented, should include proper safety checks.
        """
        # Future: Safe formula evaluation
        # For now, just return None
        pass
    
    def _validate_formula(self, formula: str) -> bool:
        """
        Validate formula syntax (for future use).
        
        Args:
            formula: Formula string to validate
        
        Returns:
            True if valid, raises exception otherwise
        """
        # Future: Validate formula syntax
        # Check for allowed operations, variable references, etc.
        pass
    
    def _evaluate_linked_parameters(self, source_context: str, 
                                   source_param: str, source_value: Any):
        """
        Evaluate and update linked parameters (for future use).
        
        Args:
            source_context: Context of changed parameter
            source_param: Name of changed parameter
            source_value: New value of changed parameter
        """
        # Future: Find enabled links where this param is source
        # Evaluate formulas and update target parameters
        pass
    
    def clear_context(self, context: str):
        """Clear all parameters for a context"""
        if context == "doors":
            self.doors_params.clear()
        elif context == "frames":
            self.frames_params.clear()
    
    def clear_all(self):
        """Clear all parameters and links"""
        self.doors_params.clear()
        self.frames_params.clear()
        self.links.clear()
