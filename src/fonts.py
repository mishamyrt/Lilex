PATH='input/plex/IBM-Plex-Mono/fonts/complete/otf/'

fonts = []

for weight in [
    'Bold',
    'BoldItalic',
    'Medium',
    'MediumItalic',
    'Regular',
    'Italic',
    'Light',
    'LightItalic',
    'Text',
]:
    fonts.append(PATH + 'IBMPlexMono-' + weight + '.otf')