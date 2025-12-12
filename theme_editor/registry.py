"""
Theme Editor Registry
Manages available configuration sections.
"""

# Import sections (will happen as we create them)
# from .sections.global_settings import GlobalSection
# from .sections.buttons import ButtonsSection

class ThemeSectionRegistry:
    _sections = []
    
    @classmethod
    def register(cls, category, name, section_class):
        cls._sections.append({
            "category": category,
            "name": name,
            "class": section_class
        })
        
    @classmethod
    def get_sections(cls):
        return cls._sections
