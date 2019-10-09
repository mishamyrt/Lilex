#!/bin/bash
rm -rf build/otf/*
fontforge -lang=py -script src/ligaturize.py 2>&1 | fgrep -v 'This contextual rule applies no lookups.'