#!/bin/sh

file=fixtures/Kilbride\ PN.pdf

setup () {
  rm -f "$file.txt"
  ./ocr "$file"
}

runtests() {
  text="ARMY"
  assert 'The text file is created in the right place' [ -e "$file".txt ]
  assert "The text file contains the text \"$text\"" [ "`grep -c $text $file.txt`" != '0' ]
}

teardown () {
  rm -f "$file.txt"
}
