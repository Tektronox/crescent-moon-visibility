#!/bin/bash

CC=gcc

rm -f visibility.out
$CC -fopenmp -O3 -Wall -Werror -o visibility.out -fno-exceptions -DPIXEL_PER_DEGREE=4 visibility.cc thirdparty/astronomy.c -lm || exit $?
echo "Compilation is completed, now let's running the calculation.."

DATE_LIST=$(jq -r '.[]' dates.json)

TYPE="evening"
METHOD="yallop"

for DATE in $DATE_LIST; do
  echo "Processing date: $DATE"
  
  # Create a new filename using DATE, TYPE, and METHOD
  FILENAME="${DATE}-${TYPE}-${METHOD}.png"

  # Run the visibility.out program and generate the image with the new filename
  time ./visibility.out "$DATE" map "$TYPE" "$METHOD" "$FILENAME" || (echo "Not successful for $DATE" && continue)

  echo "Visibility calculated, blending maps for $DATE.."
  
  # Composite with the map.png using the new filename
  composite -blend 60 "$FILENAME" map.png "$FILENAME"

  # Capitalize the first letter of TYPE and METHOD for the label
  TYPE_CAP="$(tr '[:lower:]' '[:upper:]' <<< ${TYPE:0:1})${TYPE:1}"
  METHOD_CAP="$(tr '[:lower:]' '[:upper:]' <<< ${METHOD:0:1})${METHOD:1}"

  # Add text label to the image with TYPE, METHOD, and DATE
  convert -pointsize 20 -fill black -draw "gravity south text 0,0 '$TYPE_CAP, $METHOD_CAP, $DATE'" "$FILENAME" "$FILENAME"
  
  echo "Finished processing $DATE"
done

echo "All dates processed."
