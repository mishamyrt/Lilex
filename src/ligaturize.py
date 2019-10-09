import fontforge
import psMat
from glob import glob
from os import path

from ligatures import ligatures

COPYRIGHT = '''
Programming ligatures added by Mikhael Khrustik from FiraCode
FiraCode Copyright (c) 2015 by Nikita Prokopov'''

PLEX_MONO_GLOB = 'input/plex/IBM-Plex-Mono/fonts/complete/otf/*.otf'

def get_ligature_source(fontname):
    fontname = fontname.lower()
    for weight in ['Bold', 'Medium', 'Regular', 'Light']:
        if fontname.endswith('-' + weight.lower()):
            return 'input/FiraCode/distr/otf/FiraCode-%s.otf' % weight

    return 'input/FiraCode/distr/otf/FiraCode-Regular.otf'
    

class LigatureCreator(object):

    def __init__(self, font, firacode):
        self.font = font
        self.firacode = firacode
        self._lig_counter = 0

        self.firacode.em = self.font.em
        self.emwidth = self.font[ord('m')].width

    def copy_ligature_from_source(self, ligature_name):
        try:
            self.firacode.selection.none()
            self.firacode.selection.select(ligature_name)
            self.firacode.copy()
            return True
        except ValueError:
            return False

    def correct_ligature_width(self, glyph):
        scale = float(self.emwidth) / glyph.width
        glyph.transform(psMat.scale(scale, 1.0))
        glyph.width = self.emwidth

    def add_ligature(self, input_chars, ligature_name):
        if not self.copy_ligature_from_source(ligature_name):
            return

        self._lig_counter += 1
        ligature_name = 'lig.{}'.format(self._lig_counter)

        self.font.createChar(-1, ligature_name)
        self.font.selection.none()
        self.font.selection.select(ligature_name)
        self.font.paste()
        self.correct_ligature_width(self.font[ligature_name])

        self.font.selection.none()
        self.font.selection.select('space')
        self.font.copy()

        lookup_name = lambda i: 'lookup.{}.{}'.format(self._lig_counter, i)
        lookup_sub_name = lambda i: 'lookup.sub.{}.{}'.format(self._lig_counter, i)
        cr_name = lambda i: 'CR.{}.{}'.format(self._lig_counter, i)

        for i, char in enumerate(input_chars):
            self.font.addLookup(lookup_name(i), 'gsub_single', (), ())
            self.font.addLookupSubtable(lookup_name(i), lookup_sub_name(i))

            if char not in self.font:
                self.font[ord(char)].glyphname = char

            if i < len(input_chars) - 1:
                self.font.createChar(-1, cr_name(i))
                self.font.selection.none()
                self.font.selection.select(cr_name(i))
                self.font.paste()

                self.font[char].addPosSub(lookup_sub_name(i), cr_name(i))
            else:
                self.font[char].addPosSub(lookup_sub_name(i), ligature_name)

        calt_lookup_name = 'calt.{}'.format(self._lig_counter)
        self.font.addLookup(calt_lookup_name, 'gsub_contextchain', (),
            (('calt', (('DFLT', ('dflt',)),
                       ('arab', ('dflt',)),
                       ('armn', ('dflt',)),
                       ('cyrl', ('SRB ', 'dflt')),
                       ('geor', ('dflt',)),
                       ('grek', ('dflt',)),
                       ('lao ', ('dflt',)),
                       ('latn', ('CAT ', 'ESP ', 'GAL ', 'ISM ', 'KSM ', 'LSM ', 'MOL ', 'NSM ', 'ROM ', 'SKS ', 'SSM ', 'dflt')),
                       ('math', ('dflt',)),
                       ('thai', ('dflt',)))),))
        for i, char in enumerate(input_chars):
            self.add_calt(calt_lookup_name, 'calt.{}.{}'.format(self._lig_counter, i),
                '{prev} | {cur} @<{lookup}> | {next}',
                prev = ' '.join(cr_name(j) for j in range(i)),
                cur = char,
                lookup = lookup_name(i),
                next = ' '.join(input_chars[i+1:]))

        # Add ignore rules
        self.add_calt(calt_lookup_name, 'calt.{}.{}'.format(self._lig_counter, i+1),
            '| {first} | {rest} {last}',
            first = input_chars[0],
            rest = ' '.join(input_chars[1:]),
            last = input_chars[-1])
        self.add_calt(calt_lookup_name, 'calt.{}.{}'.format(self._lig_counter, i+2),
            '{first} | {first} | {rest}',
            first = input_chars[0],
            rest = ' '.join(input_chars[1:]))

    def add_calt(self, calt_name, subtable_name, spec, **kwargs):
        spec = spec.format(**kwargs)
        self.font.addContextualSubtable(calt_name, subtable_name, 'glyph', spec)


def replace_sfnt(font, key, value):
    font.sfnt_names = tuple(
        (row[0], key, value)
        if row[1] == key
        else row
        for row in font.sfnt_names
    )

def update_font_metadata(font, new_name):
    try:
        suffix = font.fontname.split('-')[1]
    except IndexError:
        suffix = None

    if suffix:
        font.fullname = "%s %s" % (new_name, suffix)
        font.fontname = "%s-%s" % (new_name.replace(' ', ''), suffix)
    else:
        font.fullname = "%s %s" % (new_name, 'Regular') 
        font.fontname = "%s-Regular" % new_name.replace(' ', '')

    print("Ligaturizing font %s" % (path.basename(font.path)))

    font.copyright += COPYRIGHT
    replace_sfnt(font, 'UniqueID', '%s; Ligaturized' % font.fullname)
    replace_sfnt(font, 'Preferred Family', new_name)
    replace_sfnt(font, 'Compatible Full', new_name)
    replace_sfnt(font, 'WWS Family', new_name)

def ligaturize_font(input_font_file, output_dir,
                    output_name, **kwargs):
    font = fontforge.open(input_font_file)

    ligature_font_file = get_ligature_source(font.fontname)

    if output_name:
        name = output_name
    else:
        name = font.familyname

    update_font_metadata(font, name)

    print('    ...using ligatures from %s' % ligature_font_file)
    firacode = fontforge.open(ligature_font_file)

    creator = LigatureCreator(font, firacode, **kwargs)
    ligature_length = lambda lig: len(lig['chars'])
    for lig_spec in sorted(ligatures, key = ligature_length):
        try:
            creator.add_ligature(lig_spec['chars'], lig_spec['ligature_name'])
        except Exception as e:
            print('Exception while adding ligature: {}'.format(lig_spec))
            raise

    font.upos += font.uwidth

    if input_font_file[-4:].lower() == '.otf':
        output_font_type = '.otf'
    else:
        output_font_type = '.ttf'

    # Generate font & move to output directory
    output_font_file = path.join(output_dir, output_font_type[1:], font.fontname + output_font_type)
    print("    ...saving to '%s' (%s)" % (output_font_file, font.fullname))
    font.generate(output_font_file)

files = glob(PLEX_MONO_GLOB)
for input_file in files:
    ligaturize_font(
      input_file, output_dir='build/',
      output_name='Lilex')