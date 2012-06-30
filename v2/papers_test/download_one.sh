#!/bin/sh

# The server.example directory must be served at localhost:5678
# The pdf directory must be empty.

. ./papers.sh

runtests() {
  permit=MVN-foo-bar-baz
  date=2012-04-01
  paper \
    --papertype public_notice \
    --url localhost:5678/Kilbride\ PN.pdf \
    --permit $permit \
    --date $date
  assert 'Something has been saved' [ -e pdfs/$permit/public_notice-$date.pdf ]
  assert 'Something md5sum has been created' [ -e pdfs/$permit/public_notice-$date.pdf.md5 ]
  cd pdfs/$permit
  assert 'md5sum matches' md5sum --status --check public_notice-$date.pdf.md5
  cd -
  assert 'The appropriate short link has been created' [ "pdfs/$permit/public_notice-$date.pdf" = "`readlink pdfs/$permit/public_notice.pdf`" ]
}
