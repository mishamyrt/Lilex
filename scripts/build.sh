#!/bin/bash
rm -rf build/
mkdir build/
mkdir build/otf
fontforge -lang=py -script src/ligaturize.py 2>&1 | fgrep -v 'This contextual rule applies no lookups.'
python3 src/fix-meta.py