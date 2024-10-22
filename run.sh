#!/bin/bash

CC=gcc
OPEN=xdg-open
if [[ "$OSTYPE" == "darwin"* ]]; then
    CC="/opt/homebrew/opt/llvm/bin/clang -L/opt/homebrew/opt/llvm/lib -fno-rtti" # -mllvm -polly
    OPEN=open
fi

rm -f visibility.out
$CC -fopenmp -O3 -Wall -Werror -o visibility.out -fno-exceptions -DPIXEL_PER_DEGREE=4 visibility.cc thirdparty/astronomy.c -lm || exit $?

echo "Compiliation is completed, now let's running the calculation.."

# Define an array of dates
# DATES=("2025-03-29" "2025-03-30" "2025-03-31"
#        "2025-09-21" "2025-09-22" "2025-09-23")

DATES=("2024-09-30" "2024-09-29")

TYPE="evening"
METHOD="yallop"

for DATE in "${DATES[@]}"; do
  echo "Processing date: $DATE"
  
  # Create a new filename using DATE, TYPE, and METHOD
  FILENAME="${DATE}-${TYPE}-${METHOD}.png"

  # Run the visibility.out program and generate the image with the new filename
  time ./visibility.out $DATE map $TYPE $METHOD $FILENAME || (echo "Not successful for $DATE" && continue)

  echo "visibility calculated, blending maps for $DATE.."
  
  # Composite with the map.png using the new filename
  composite -blend 60 $FILENAME map.png $FILENAME

  # Capitalize the first letter of TYPE and METHOD for the label
  TYPE_CAP="$(tr '[:lower:]' '[:upper:]' <<< ${TYPE:0:1})${TYPE:1}"
  METHOD_CAP="$(tr '[:lower:]' '[:upper:]' <<< ${METHOD:0:1})${METHOD:1}"

  # Add text label to the image with TYPE, METHOD, and DATE
  convert -pointsize 20 -fill black -draw "gravity south text 0,0 '$TYPE_CAP, $METHOD_CAP, $DATE'" $FILENAME $FILENAME
  
  echo "Finished processing $DATE"
done

echo "All dates processed."