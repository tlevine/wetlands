#!/bin/sh

# The server.example directory must be served at localhost:5678
# The pdf directory must be empty.

. ./papers.sh

setup() {
  rm -Rf pdfs/MVN-foo-bar-baz
}

runtests() {
  permit=MVN-foo-bar-baz
  date=2012-04-01

  paper \
    --papertype public_notice \
    --url localhost:5678/Kilbride\ PN.pdf \
    --permit $permit \
    --date $date

  assert 'Something has been saved on first download' [ -e pdfs/$permit/public_notice-$date.pdf ]
  assert 'Some md5sum has been created on first download' [ -e pdfs/$permit/public_notice-$date.pdf.md5 ]
  cd pdfs/$permit
  assert 'md5sum matches on first download' md5sum --status --check public_notice-$date.pdf.md5
  cd - > /dev/null
  assert 'The appropriate short link has been created on first download' [ "pdfs/$permit/public_notice-$date.pdf" = "`readlink pdfs/$permit/public_notice.pdf`" ]

  paper \
    --papertype public_notice \
    --url localhost:5678/Kilbride\ PN.pdf \
    --permit $permit \
    --date $date

  assert 'Something has been saved on second download' [ -e pdfs/$permit/public_notice-$date.pdf ]
  assert 'Some md5sum has been created on second download' [ -e pdfs/$permit/public_notice-$date.pdf.md5 ]
  cd pdfs/$permit
  assert 'md5sum matches on second download' md5sum --status --check public_notice-$date.pdf.md5
  cd - > /dev/null
  assert 'The appropriate short link has been created on second download' [ "pdfs/$permit/public_notice-$date.pdf" = "`readlink pdfs/$permit/public_notice.pdf`" ]
}
