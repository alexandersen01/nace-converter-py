from NACEConverter import NACEConverter

converter = NACEConverter()
print(converter.get_description('01.1'))  # Should print: Growing of non-perennial crops
print(converter.get_description('011'))   # Same result, works without dots!
print(converter.search_codes('painting')) # Should find painting-related codes