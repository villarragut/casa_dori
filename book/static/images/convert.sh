#!/bin/bash

# format images
echo -n "Formatting images to 850x568... "
for f in casa_*.jpg; do convert "$f" -resize "850x568^" -gravity center -crop 850x568+0+0 +repage "$f";done
echo "Done"

# generate gif
echo -n "Generating gif... "
convert -delay 200 casa_*.jpg casa.gif
echo "Done"
