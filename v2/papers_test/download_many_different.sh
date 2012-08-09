#!/bin/sh

. ./papers.sh

setup() {
  rm -Rf pdfs/MVN-foo-bar-baz
}

runtests() {
  permit=MVN-foo-bar-baz
  paper \
    --papertype public_notice \
    --url http://localhost:5678/Kilbride\ PN.pdf \
    --permit $permit \
    --date 2012-05-28

  paper \
    --papertype public_notice \
    --url http://localhost:5678/listing.html \
    --permit $permit \
    --date 2012-06-01

  assert 'Something has been saved for May 28' [ -e pdfs/$permit/public_notice-2012-05-28.pdf ]
  assert 'Something has been saved for June 1' [ -e pdfs/$permit/public_notice-2012-06-01.pdf ]
  assert 'md5sum has been saved for May 28' [ -e pdfs/$permit/public_notice-2012-05-28.pdf.md5 ]
  assert 'md5sum has been saved for June 1' [ -e pdfs/$permit/public_notice-2012-06-01.pdf.md5 ]
  cd pdfs/$permit
  assert 'The appropriate short link has been created' [ "`readlink public_notice.pdf`" = "public_notice-2012-06-01.pdf" ]
}
