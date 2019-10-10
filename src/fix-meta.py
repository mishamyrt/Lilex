from glob import glob
from fontTools.ttLib import TTFont

LILEX_OTF_GLOB = 'build/otf/*.otf'

FAMILY_RELATED_IDS = dict(
    FONT_NAME=1,
    VERSION=5,
    DESIGNER=9,
    DESIGNER_URL=11,
    MANUFACTOR_URL=12,
    TRADEMARK=7
)


def get_designers(table):
    return str(table.getName(
        nameID=FAMILY_RELATED_IDS['DESIGNER'],
        platformID=1,
        platEncID=0,
        langID=0,
    ))

def get_font_name(table):
    return str(table.getName(
        nameID=FAMILY_RELATED_IDS['FONT_NAME'],
        platformID=1,
        platEncID=0,
        langID=0,
    )).replace('IBM Plex Mono', 'Lilex')


def fix_meta(font_path):
    font = TTFont(font_path)
    table = font["name"]
    designers = get_designers(table) + ', Nikita Prokopov, Mikhael Khrustik'
    font_name = get_font_name(table)
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
        if name_id == FAMILY_RELATED_IDS['FONT_NAME']:
            rec.string = font_name
        if name_id == FAMILY_RELATED_IDS['TRADEMARK']:
            table.names.remove(rec)

    font.save(font_path)


fix_meta('build/otf/Lilex-Regular.otf')

files = glob(LILEX_OTF_GLOB)
for input_file in files:
    fix_meta(input_file)
