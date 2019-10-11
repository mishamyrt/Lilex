#!/bin/bash
rm -rf build/
mkdir build/
mkdir build/otf
mkdir build/ttf-not_hinted
mkdir build/ttf
fontforge -lang=py -script src/build.py 2>&1 | fgrep -v 'This contextual rule applies no lookups.'
python3 src/fix-meta.py
python3 src/convert.py

for input_file in build/ttf-not_hinted/*.ttf
do
	output_file=build/ttf/$(basename "$input_file")
    ttfautohint -I $input_file $output_file --stem-width-mode nnn --composites
    gftools fix-dsig --autofix $output_file
done

rm -rf build/ttf-not_hinted