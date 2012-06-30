#!/bin/sh

. pdftext.sh

file=fixtures/Kilbride\ PN.pdf

setup () {
  rm -f "$file.txt"
  pdftext "$file"
}

runtests() {
  text="ARMY"
  assert 'The text file is created in the right place' [ -e fixtures/Kilbride\ PN.pdf.txt ]
  assert "The text file contains the text \"$text\"" \
    [ "`grep -c \"$text\" fixtures/Kilbride\ PN.pdf.txt`" != '0' ]
}

#teardown () {
#  rm -f "$file.txt"
#}
