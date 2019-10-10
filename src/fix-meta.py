from glob import glob
from fontTools.ttLib import TTFont

LILEX_OTF_GLOB = 'build/otf/*.otf'

FAMILY_RELATED_IDS = dict(
    VERSION=5,
    DESIGNER=9,
    DESIGNER_URL=11,
    MANUFACTOR_URL=12
)


def get_designers(table):
    return str(table.getName(
        nameID=FAMILY_RELATED_IDS['DESIGNER'],
        platformID=1,
        platEncID=0,
        langID=0,
    ))


def fix_meta(font_path):
    font = TTFont(font_path)
    table = font["name"]
    designers = get_designers(table) + ', Nikita Prokopov, Mikhael Khrustik'
    for rec in table.names:
        name_id = rec.nameID
        if name_id not in FAMILY_RELATED_IDS.values():
            continue
        if name_id == FAMILY_RELATED_IDS['VERSION']:
            rec.string = 'Version 1.000'
        if name_id == FAMILY_RELATED_IDS['DESIGNER_URL'] or name_id == FAMILY_RELATED_IDS['MANUFACTOR_URL']:
            rec.string = 'https://myrt.co'
        if name_id == FAMILY_RELATED_IDS['DESIGNER']:
            rec.string = designers

    font.save(font_path)


fix_meta('build/otf/Lilex-Regular.otf')

files = glob(LILEX_OTF_GLOB)
for input_file in files:
    fix_meta(input_file)
