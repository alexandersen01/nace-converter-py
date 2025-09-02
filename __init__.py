"""
NACE Converter Package

A Python package for converting NACE codes to their plaintext descriptions
and searching for codes by keywords.

Usage:
    import naceconverter as nc
    
    # Get description for a code
    description = nc.get_description("01.1")
    
    # Search for codes
    results = nc.search_codes("farming")
"""

from .NACEConverter import NACEConverter

# Create a singleton instance for convenient module-level access
_converter = None

def _get_converter():
    """Get or create the singleton converter instance."""
    global _converter
    if _converter is None:
        _converter = NACEConverter()
    return _converter

def get_description(code: str):
    """
    Get the plaintext description for a NACE code.
    
    Args:
        code: The NACE code to look up (with or without dots)
        
    Returns:
        The description of the code, or None if not found
        
    Examples:
        >>> import naceconverter as nc
        >>> nc.get_description("01.1")
        'Growing of non-perennial crops'
        >>> nc.get_description("011")  # Works without dots
        'Growing of non-perennial crops'
    """
    return _get_converter().get_description(code)

def get_full_info(code: str):
    """
    Get complete information for a NACE code.
    
    Args:
        code: The NACE code to look up (with or without dots)
        
    Returns:
        Dictionary with all information about the code, or None if not found
        
    Examples:
        >>> import naceconverter as nc
        >>> info = nc.get_full_info("01.1")
        >>> print(info['name'])
        'Growing of non-perennial crops'
    """
    return _get_converter().get_full_info(code)

def search_codes(keyword: str, max_results=None):
    """
    Search for NACE codes containing a keyword.
    
    Args:
        keyword: The search term
        max_results: Maximum number of results to return
        
    Returns:
        List of dictionaries with matching codes
        
    Examples:
        >>> import naceconverter as nc
        >>> results = nc.search_codes("painting")
        >>> for r in results:
        ...     print(f"{r['code']}: {r['description']}")
        43.34: Painting and glazing
    """
    return _get_converter().search_codes(keyword, max_results)

def search_code(keyword: str, max_results=None):
    """
    Alias for search_codes (singular form for convenience).
    
    Args:
        keyword: The search term
        max_results: Maximum number of results to return
        
    Returns:
        List of dictionaries with matching codes
        
    Examples:
        >>> import naceconverter as nc
        >>> print(nc.search_code('painting'))
        [{'code': '43.34', 'description': 'Painting and glazing', 'level': 4}, ...]
    """
    return search_codes(keyword, max_results)

def get_all_codes():
    """
    Get a list of all available NACE codes.
    
    Returns:
        List of all NACE codes in the dataset
        
    Examples:
        >>> import naceconverter as nc
        >>> all_codes = nc.get_all_codes()
        >>> print(f"Total codes: {len(all_codes)}")
    """
    return _get_converter().get_all_codes()

def get_codes_by_level(level: int):
    """
    Get all NACE codes at a specific hierarchical level.
    
    Args:
        level: The hierarchy level (1-4 typically)
        
    Returns:
        List of dictionaries with codes at the specified level
        
    Examples:
        >>> import naceconverter as nc
        >>> level_2_codes = nc.get_codes_by_level(2)
    """
    return _get_converter().get_codes_by_level(level)

def get_children(parent_code: str):
    """
    Get all direct children of a NACE code.
    
    Args:
        parent_code: The parent NACE code
        
    Returns:
        List of dictionaries with child codes
        
    Examples:
        >>> import naceconverter as nc
        >>> children = nc.get_children("01")
        >>> for child in children:
        ...     print(f"{child['code']}: {child['description']}")
    """
    return _get_converter().get_children(parent_code)

# Export main classes and functions
__all__ = [
    'NACEConverter',
    'get_description',
    'get_full_info',
    'search_codes',
    'search_code',
    'get_all_codes',
    'get_codes_by_level',
    'get_children'
]

__version__ = '1.0.0'