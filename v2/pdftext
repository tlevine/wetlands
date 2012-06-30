#!/bin/sh

set -e

FILE="$1"

# Extract images
pdfimages -j "$FILE" "$FILE"

# Extract text to `echo $FILE|sed s/pdf$/txt/`
pdftotext "$FILE"
mv "`echo \"$FILE\"|sed s/pdf$/txt/`" "$FILE.txt"

# OCR
for file in "$FILE"-[0-9][0-9][0-9].jpg
  do
  tesseract "$file" "$file"
  cat "$file.txt" >> "$FILE.txt"
done
