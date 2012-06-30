#!/bin/sh

ocr

file=pdf.example/aoseutaoeu/aoeuoaeu.pdf

setup () {
  rm -f $file
  ./ocr $file
}

runtests() {
  text=aoeuaoeuoaeu
  assert 'The text file is created in the right place' [ -e "$file".txt ]
  assert "The text file contains the text \"$text\"" [ "`grep -c $text $file.txt`" != '0' ]
}
