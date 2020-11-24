
'''
Class helpers
'''

from typing import List

denied_symbols = [
    '.notdef',
    'NULL',
    'CR'
]

def is_space (symbol: str) -> bool:
    return \
        '.liga' in symbol or \
        symbol in denied_symbols or \
        'space' in symbol

def get_not_space_glyphs (symbols: List[str]) -> List[str]:
    return list(filter(lambda x: not is_space(x), symbols))
