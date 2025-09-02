# NACE Converter

A Python package for converting NACE codes to their plaintext descriptions and searching for codes by keywords.

## What is NACE?

NACE (Nomenclature of Economic Activities) is the European statistical classification of economic activities. NACE codes are used to classify business activities for statistical purposes.

## Installation

```bash
pip install naceconverter
```

## Quick Start

```python
import naceconverter as nc

# Get description for a NACE code
description = nc.get_description("01.1")
print(description)  # "Growing of non-perennial crops"

# Works with or without dots
description = nc.get_description("011")
print(description)  # "Growing of non-perennial crops"

# Search for codes containing a keyword
results = nc.search_code('painting')
for result in results:
    print(f"{result['code']}: {result['description']}")

# Get full information about a code
info = nc.get_full_info("01.1")
print(info)
# {'code': '01.1', 'name': 'Growing of non-perennial crops', 'level': 3, ...}
```

## Features

- **Flexible Code Lookup**: Handles codes with or without dots (e.g., "01.30" and "0130" return the same result)
- **Fast Search**: Search for NACE codes by keywords in descriptions
- **Complete Information**: Access full details including hierarchy level, parent codes, and validity dates
- **Zero Dependencies**: Pure Python implementation with no external dependencies
- **Included Data**: NACE codes data is bundled with the package

## API Reference

### Module-level Functions

#### `get_description(code: str) -> Optional[str]`

Get the plaintext description for a NACE code.

#### `search_code(keyword: str, max_results: Optional[int] = None) -> List[Dict]`

Search for NACE codes containing a keyword. Returns a list of matching codes with their descriptions.

#### `search_codes(keyword: str, max_results: Optional[int] = None) -> List[Dict]`

Alias for `search_code()` that returns multiple results.

#### `get_full_info(code: str) -> Optional[Dict]`

Get complete information for a NACE code including level, parent code, notes, and validity dates.

### NACEConverter Class

For more advanced usage, you can work directly with the `NACEConverter` class:

```python
from naceconverter.NACEConverter import NACEConverter

converter = NACEConverter()
description = converter.get_description("01.1")
```

## Examples

### Finding all codes related to agriculture

```python
import naceconverter as nc

results = nc.search_code('agriculture')
for r in results:
    print(f"Code: {r['code']}, Level: {r['level']}, Description: {r['description']}")
```

### Getting parent-child relationships

```python
import naceconverter as nc

info = nc.get_full_info("01.11")
parent_code = info['parentCode']
parent_info = nc.get_full_info(parent_code)
print(f"Parent: {parent_info['name']}")
```

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
