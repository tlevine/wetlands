#!/bin/sh

. ./papers.sh

runtests() {
  permit=MVN-a93409234
  paper \
    --papertype public_notice \
    --url localhost:5678/thuho.pdf \
    --permit $permit \
    --date 2012-05-28
  paper \
    --papertype public_notice \
    --url localhost:5678/thuho.pdf \
    --permit $permit \
    --date 2012-06-01

  assert 'Something has been saved for May 28' [ -e pdfs/$permit/public_notice-2012-05-28.pdf ]
  assert 'Something has been saved for June 1' [ -e pdfs/$permit/public_notice-2012-06-01.pdf ]
  assert 'md5sum has been saved for May 28' [ -e pdfs/$permit/public_notice-2012-05-28.pdf.md5 ]
  assert 'md5sum has been saved for June 1' [ -e pdfs/$permit/public_notice-2012-06-01.pdf.md5 ]
  assert 'The appropriate short link has been created' [ "`readlink pdfs/$permit/public_notice.pdf`" = "pdfs/$permit/public_notice-2012-06-01.pdf" ]
}
