#!/bin/sh

# Converts SVG files into PNG files
# bash svg_to_png.sh

for file in *.svg
do
    filename=${file%.svg}
    echo $filename
    convert $file $filename".png"
done