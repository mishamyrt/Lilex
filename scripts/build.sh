#!/bin/bash
rm -rf build

BUILD_DIRECTORY=build
VF_DIRECTORY=$BUILD_DIRECTORY/variable_ttf
TTF_DIRECTORY=$BUILD_DIRECTORY/ttf
OTF_DIRECTORY=$BUILD_DIRECTORY/otf

LILEX_VF=$VF_DIRECTORY/Lilex-VF.ttf
LILEX_DESIGNSPACE=source/Lilex.designspace

fontmake -m $LILEX_DESIGNSPACE -o variable --output-dir $VF_DIRECTORY
gftools fix-vf-meta $LILEX_VF
gftools fix-nonhinting $LILEX_VF $LILEX_VF
gftools fix-gasp --autofix $LILEX_VF
gftools fix-dsig --autofix $LILEX_VF

tempFiles=$(ls $VF_DIRECTORY/*.fix && ls $VF_DIRECTORY/*-gasp*)
for temp in $tempFiles
do
    rm -rf $temp
done

fontmake -m $LILEX_DESIGNSPACE -o ttf --output-dir $TTF_DIRECTORY -i

statics=$(ls $TTF_DIRECTORY/*.ttf)
for file in $statics; do 
    echo "fix DSIG in " ${file}
    gftools fix-dsig --autofix ${file}

    echo "TTFautohint " ${file}
    # autohint with detailed info
    hintedFile=${file/".ttf"/"-hinted.ttf"}
    ttfautohint -I ${file} ${hintedFile} --stem-width-mode nnn --composites --windows-compatibility
    cp ${hintedFile} ${file}
    rm -rf ${hintedFile}
done

fontmake -m $LILEX_DESIGNSPACE -o otf --output-dir $OTF_DIRECTORY -i