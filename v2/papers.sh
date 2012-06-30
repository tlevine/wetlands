#!/bin/sh

paper() {
  set -e

  # Parametrize this.
  permit=MVN-foo-bar-baz
  date=2012-04-01
  papertype=public_notice
  url=localhost:5678/Kilbride\ PN.pdf

  dir="pdfs/$permit"
  file="pdfs/$permit/$papertype-$date.pdf"
  link="pdfs/$permit/$papertype.pdf"

  mkdir -p "$dir"
  wget -O "$file" "$url"
  (
    cd $dir
    md5sum "$papertype-$date.pdf" > "$papertype-$date.pdf.md5"
  )

  if [ -h $link ] && [ "`cut -d \  -f 1 $file.md5`" = "`cut -d \  -f 1 $link.md5`" ]
    then
    # If this is the same as the previous file,

    # delete the current file
    rm "$file" "$file.md5"

    # and update the "last seen" field in the database.
    # mongo wetlands --eval "db.permits"
  else
    # If it's different or new, change the links
    rm -f "$link" "$link.md5"
    ln -s "$file" "$link"
    ln -s "$file.md5" "$link.md5"

    # and update the "last seen" and "md5sum" fields in the database.
    # mongo wetlands --eval "db.permits"

  fi
}

