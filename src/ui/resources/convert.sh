#!/bin/sh
# convert svg to certain size icon
size_l="56x56"
size_m="12x12"

convert +antialias -background transparent -resize $size_l heart.svg heart.png
convert +antialias -background transparent -resize $size_l  -channel r -evaluate set 100% heart.svg hearted.png
convert +antialias -background transparent -resize $size_l trash.svg trash.png
convert +antialias -background transparent -resize $size_l skip.svg skip.png
convert -negate +antialias -background transparent -resize $size_m play.svg play.png
convert -negate +antialias -background transparent -resize $size_m pause.svg pause.png
convert +antialias -background transparent -resize $size_m volume1.svg volume1.png
convert +antialias -background transparent -resize $size_m volume2.svg volume2.png
convert +antialias -background transparent -resize $size_m volume3.svg volume3.png
convert +antialias -background transparent -resize $size_l share.svg share.png
