import re
from string import Template

FIRA_CODE_GLYPHS_FILE = 'input/fira/FiraCode.glyphs'
OUTPUT_LIGATURES_FILE = 'src/ligatures.py'

f = open(FIRA_CODE_GLYPHS_FILE, 'r')
glyphs_content = f.read()
f.close()

pattern = re.compile('[a-zA-Z_]+.liga')
ligatures = set(pattern.findall(glyphs_content))

ligature_template = Template(
'''    {
        # $preview
        'chars': [$symbols],
        'ligature_name': '$ligature'
    },
''')


def symbol_to_glyph(symbol):
    return {
        'less': '<',
        'greater': '>',
        'equal': '=',
        'bar': '|',
        'slash': '/',
        'numbersign': '#',
        'colon': ':',
        'at': '@',
        'F': 'F',
        'l': 'l',
        'f': 'f',
        'i': 'i',
        'T': 'T',
        'j': 'j',
        'w': 'w',
        't': 't',
        'percent': '%',
        'backslash': '\\',
        'question': '?',
        'dollar': '$',
        'asterisk': '*',
        'exclam': '!',
        'period': '.',
        'underscore': '_',
        'semicolon': ';',
        'plus': '+',
        'hyphen': '-',
        'parenleft': '(',
        'parenright': ')',
        'bracketleft': '[',
        'bracketright': ']',
        'braceleft': '{',
        'braceright': '}',
        'ampersand': '&',
        'asciicircum': '^',
        'asciitilde': '~'
    }[symbol]


def build_ligature_preview(symbols):
    output = ''
    for symbol in symbols:
        output += symbol_to_glyph(symbol)
    return output


ligature_list = ''
for ligature in ligatures:
    symbols = ligature.split('.')[0].split('_')
    preview = build_ligature_preview(symbols)
    symbols = map(lambda symbol: '\'' + symbol + '\'', symbols)
    ligature_list += ligature_template.substitute(
        ligature=ligature,
        symbols=', '.join(symbols),
        preview=preview
    )
f = open(OUTPUT_LIGATURES_FILE, 'w+')
f.write('''
ligatures = [
%s
]''' % (ligature_list[:-2]))
f.close()