#!/bin/bash
rm -rf build/
mkdir build/
mkdir build/otf

fontmake -m source/Lilex.designspace  -o variable --output-dir build/variable_ttf