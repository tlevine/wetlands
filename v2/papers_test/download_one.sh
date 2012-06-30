#!/bin/sh

# The server.example directory must be served at localhost:5678
# The pdf directory must be empty.

. papers.sh


runtests() {
  permit=MVN-a93409234
  date=2012-06-01
  paper
    --papertype public_notice \
    --url localhost:5678/thuho.pdf \
    --permit $permit \
    --date $date
  assert 'Something has been saved' [ -e pdfs/$permit/public_notice-$date.pdf ]
  assert 'Something md5sum has been created' [ -e pdfs/$permit/public_notice-$date.pdf.md5 ]
  assert 'md5sum matches' false
  assert 'The appropriate short link has been created' false
}
