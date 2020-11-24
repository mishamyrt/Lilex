"""
Lilex builder performs actions that can be automated.
Generates the ligature code, inserts the rest of the code from 'fea' files, etc.
"""

from glyphs import GlyphsFile
from fea import read_feature, read_class
from ligatures import render_ligature_lookups

FILE_PATH = 'Lilex.glyphs'
features = [
    'ss01',
    'ss02',
    'ss03',
    'ss04',
    'ss05'
]

classes = [
    'numbers_hex'
]

font = GlyphsFile(FILE_PATH)

# Fill 'calt' feature
font.set_feature('calt', (
    f'{render_ligature_lookups(font.ligatures)}\n'
    f'{read_feature("calt/colon")}\n'
    f'{read_feature("calt/multiply")}\n'
))

# Fill other features
for file in features:
    font.set_feature(file, read_feature(file))
# Fill classes
for file in classes:
    font.set_class(file, read_class(file))

# Write
font.flush()
print(f'{FILE_PATH} is regenerated.')
