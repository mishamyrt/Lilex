#!/bin/bash
rm -rf build/otf/*
python3 src/ligaturize.py 2>&1 | fgrep -v 'This contextual rule applies no lookups.'