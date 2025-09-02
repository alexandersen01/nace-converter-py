"""
NACE Code Converter
====================

A Python package for converting NACE codes to their plaintext descriptions
and searching for codes by keywords.

NACE (Nomenclature of Economic Activities) is the European statistical 
classification of economic activities.
"""

import csv
import os
from pathlib import Path
from typing import List, Dict, Optional, Union
import re


class NACEConverter:
    """
    A converter class for NACE codes.
    
    This class provides functionality to:
    - Convert NACE codes to their plaintext descriptions
    - Search for NACE codes by keywords
    - Access hierarchical information about NACE codes
    
    The NACE codes data is loaded from the nacecodes.csv file.
    
    Attributes:
        codes_dict (dict): Dictionary mapping codes to their full information
        normalized_codes (dict): Maps normalized codes to original codes
        search_index (dict): Inverted index for efficient text searching
    
    Examples:
        >>> converter = NACEConverter()
        >>> converter.get_description("01.1")
        'Growing of non-perennial crops'
        
        >>> converter.search_codes("farming")
        [{'code': '01.5', 'description': 'Mixed farming', 'level': 3}, ...]
    """
    
    def __init__(self, csv_path: Optional[str] = None):
        """
        Initialize the NACE converter.
        
        Args:
            csv_path: Optional path to the nacecodes.csv file.
                     If not provided, looks for the file in the same directory.
        
        Raises:
            ValueError: If the CSV data has an unexpected format
            FileNotFoundError: If the CSV file cannot be found
        """
        self.codes_dict = {}
        self.normalized_codes = {}  # Maps normalized codes to original codes
        self.search_index = {}
        self._load_data(csv_path)
        self._build_search_index()
    
    def _find_csv_path(self) -> str:
        """
        Find the path to the nacecodes.csv file.
        
        Returns:
            str: Path to the CSV file
            
        Raises:
            FileNotFoundError: If the file cannot be found
        """
        # Get the directory where this module is located
        module_dir = Path(__file__).parent
        
        # Try multiple possible locations
        possible_paths = [
            module_dir / 'nacecodes.csv',  # Same directory as this file
            Path('nacecodes.csv'),  # Current working directory
            module_dir / 'data' / 'nacecodes.csv',  # data subdirectory
        ]
        
        for path in possible_paths:
            if path.exists():
                return str(path)
        
        raise FileNotFoundError(
            f"nacecodes.csv not found. Searched in: {[str(p) for p in possible_paths]}"
        )
    
    def _clean_value(self, value):
        """
        Clean a value from the CSV by handling None and stripping quotes.
        
        Args:
            value: The value to clean (may be None or string)
            
        Returns:
            Cleaned string value
        """
        if value is None:
            return ''
        return str(value).strip('"')
    
    def _load_data(self, csv_path: Optional[str] = None):
        """
        Load NACE codes from CSV file.
        
        Args:
            csv_path: Path to the CSV file
            
        Raises:
            FileNotFoundError: If the file doesn't exist
            ValueError: If the CSV format is unexpected
        """
        if csv_path is None:
            csv_path = self._find_csv_path()
        
        if not Path(csv_path).exists():
            raise FileNotFoundError(f"CSV file not found at: {csv_path}")
        
        try:
            with open(csv_path, 'r', encoding='utf-8') as f:
                # Handle semicolon-separated CSV
                reader = csv.DictReader(f, delimiter=';')
                
                for row in reader:
                    # Clean the data - handle None values and remove quotes
                    code = self._clean_value(row.get('code'))
                    
                    if not code:  # Skip empty codes
                        continue
                    
                    # Parse level, handling None and empty strings
                    level_str = self._clean_value(row.get('level'))
                    try:
                        level = int(level_str) if level_str else 0
                    except ValueError:
                        level = 0
                    
                    self.codes_dict[code] = {
                        'code': code,
                        'parentCode': self._clean_value(row.get('parentCode')),
                        'level': level,
                        'name': self._clean_value(row.get('name')),
                        'shortName': self._clean_value(row.get('shortName')),
                        'notes': self._clean_value(row.get('notes')),
                        'validFrom': self._clean_value(row.get('validFrom')),
                        'validTo': self._clean_value(row.get('validTo'))
                    }
                    
                    # Store normalized version for flexible lookup
                    normalized = self._normalize_code(code)
                    self.normalized_codes[normalized] = code
        
        except Exception as e:
            raise ValueError(f"Error reading CSV file: {e}")
        
        if not self.codes_dict:
            raise ValueError("No NACE codes were loaded from the CSV file")
    
    def _normalize_code(self, code: str) -> str:
        """
        Normalize a NACE code by removing dots and converting to uppercase.
        
        Args:
            code: The code to normalize
            
        Returns:
            Normalized code without dots
            
        Examples:
            >>> _normalize_code("01.30")
            "0130"
            >>> _normalize_code("A")
            "A"
        """
        return code.replace('.', '').replace('-', '').upper().strip()
    
    def _build_search_index(self):
        """
        Build an inverted index for efficient text searching.
        
        Creates a mapping from words to the codes that contain them.
        """
        for code, info in self.codes_dict.items():
            # Combine searchable text fields
            searchable_text = ' '.join([
                info.get('name', ''),
                info.get('shortName', ''),
                info.get('notes', '')
            ]).lower()
            
            # Extract words (alphanumeric sequences)
            words = re.findall(r'\b\w+\b', searchable_text)
            
            # Add to index
            for word in words:
                if word not in self.search_index:
                    self.search_index[word] = set()
                self.search_index[word].add(code)
    
    def get_description(self, code: str) -> Optional[str]:
        """
        Get the plaintext description for a NACE code.
        
        Handles codes with or without dots (e.g., "01.30" and "0130" return same result).
        
        Args:
            code: The NACE code to look up
            
        Returns:
            The description (name) of the code, or None if not found
            
        Examples:
            >>> converter.get_description("01")
            'Crop and animal production, hunting and related service activities'
            >>> converter.get_description("01.1")
            'Growing of non-perennial crops'
            >>> converter.get_description("011")  # Same as "01.1"
            'Growing of non-perennial crops'
        """
        # Try direct lookup first
        code_clean = code.strip().strip('"')
        if code_clean in self.codes_dict:
            return self.codes_dict[code_clean]['name']
        
        # Try normalized lookup
        normalized = self._normalize_code(code)
        if normalized in self.normalized_codes:
            original_code = self.normalized_codes[normalized]
            return self.codes_dict[original_code]['name']
        
        return None
    
    def get_full_info(self, code: str) -> Optional[Dict]:
        """
        Get complete information for a NACE code.
        
        Handles codes with or without dots (e.g., "01.30" and "0130" return same result).
        
        Args:
            code: The NACE code to look up
            
        Returns:
            Dictionary with all information about the code, or None if not found
            
        Examples:
            >>> info = converter.get_full_info("01.1")
            >>> print(info['name'])
            'Growing of non-perennial crops'
            >>> info2 = converter.get_full_info("011")  # Same result
            >>> print(info2['name'])
            'Growing of non-perennial crops'
        """
        # Try direct lookup first
        code_clean = code.strip().strip('"')
        if code_clean in self.codes_dict:
            return self.codes_dict[code_clean].copy()
        
        # Try normalized lookup
        normalized = self._normalize_code(code)
        if normalized in self.normalized_codes:
            original_code = self.normalized_codes[normalized]
            return self.codes_dict[original_code].copy()
        
        return None
    
    def search_codes(self, keyword: str, max_results: Optional[int] = None) -> List[Dict]:
        """
        Search for NACE codes containing a keyword.
        
        Performs case-insensitive search across code names, short names, and notes.
        
        Args:
            keyword: The search term (case-insensitive)
            max_results: Maximum number of results to return (None for all)
            
        Returns:
            List of dictionaries with matching codes, sorted by relevance.
            Each dictionary contains 'code', 'description', and 'level'.
            
        Examples:
            >>> converter.search_codes("painting")
            [{'code': '43.34', 'description': 'Painting and glazing', 'level': 4}, ...]
            
            >>> converter.search_codes("agriculture", max_results=5)
            # Returns up to 5 agriculture-related codes
        """
        keyword = keyword.lower().strip()
        results = []
        scores = {}  # Track relevance scores
        
        # Direct word match from index
        matching_codes = set()
        words = re.findall(r'\b\w+\b', keyword)
        
        # Find codes containing any of the search words
        for word in words:
            if word in self.search_index:
                matching_codes.update(self.search_index[word])
        
        # Also check for partial matches and multi-word phrases
        for code, info in self.codes_dict.items():
            searchable_text = ' '.join([
                info.get('name', ''),
                info.get('shortName', ''),
                info.get('notes', '')
            ]).lower()
            
            # Calculate relevance score
            score = 0
            
            # Exact phrase match (highest priority)
            if keyword in searchable_text:
                score += 100
                matching_codes.add(code)
            
            # Individual word matches
            for word in words:
                if word in searchable_text:
                    score += 10
                    # Bonus for word at start of description
                    if info.get('name', '').lower().startswith(word):
                        score += 5
            
            # Partial word matches (lower priority)
            if score == 0:
                for word in words:
                    if len(word) > 3 and word in searchable_text:
                        score += 1
                        matching_codes.add(code)
            
            if code in matching_codes:
                scores[code] = score
        
        # Build results list
        for code in matching_codes:
            info = self.codes_dict[code]
            result = {
                'code': code,
                'description': info['name'],
                'level': info['level']
            }
            
            # Add parent code if available
            if info.get('parentCode'):
                result['parentCode'] = info['parentCode']
            
            # Add short name if different from name
            if info.get('shortName') and info['shortName'] != info['name']:
                result['shortName'] = info['shortName']
            
            results.append((scores.get(code, 0), result))
        
        # Sort by relevance score (descending) and then by code
        results.sort(key=lambda x: (-x[0], x[1]['code']))
        
        # Extract just the result dictionaries
        results = [r[1] for r in results]
        
        # Apply max_results limit if specified
        if max_results is not None and max_results > 0:
            results = results[:max_results]
        
        return results
    
    def get_all_codes(self) -> List[str]:
        """
        Get a list of all available NACE codes.
        
        Returns:
            List of all NACE codes in the dataset
            
        Examples:
            >>> all_codes = converter.get_all_codes()
            >>> print(len(all_codes))
            # Number of codes in the dataset
        """
        return sorted(list(self.codes_dict.keys()))
    
    def get_codes_by_level(self, level: int) -> List[Dict]:
        """
        Get all NACE codes at a specific hierarchical level.
        
        Args:
            level: The hierarchy level (1-4 typically)
            
        Returns:
            List of dictionaries with codes at the specified level
            
        Examples:
            >>> level_2_codes = converter.get_codes_by_level(2)
            # Returns all 2-digit codes
        """
        results = []
        for code, info in self.codes_dict.items():
            if info['level'] == level:
                results.append({
                    'code': code,
                    'description': info['name'],
                    'parentCode': info.get('parentCode', '')
                })
        
        return sorted(results, key=lambda x: x['code'])
    
    def get_children(self, parent_code: str) -> List[Dict]:
        """
        Get all direct children of a NACE code.
        
        Args:
            parent_code: The parent NACE code
            
        Returns:
            List of dictionaries with child codes
            
        Examples:
            >>> children = converter.get_children("01")
            # Returns codes like "01.1", "01.2", etc.
        """
        # Normalize the parent code for comparison
        parent_code_clean = parent_code.strip().strip('"')
        
        # Also check normalized version
        normalized_parent = self._normalize_code(parent_code)
        if normalized_parent in self.normalized_codes:
            parent_code_clean = self.normalized_codes[normalized_parent]
        
        results = []
        for code, info in self.codes_dict.items():
            if info.get('parentCode') == parent_code_clean:
                results.append({
                    'code': code,
                    'description': info['name'],
                    'level': info['level']
                })
        
        return sorted(results, key=lambda x: x['code'])