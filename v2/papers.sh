#!/bin/sh

paper() {
  set -e

  # Parametrize this.
  permit=MVN-foo-bar-baz
  date=2012-04-01
  papertype=public_notice
  url=localhost:5678/Kilbride\ PN.pdf

  dir="pdfs/$permit"
  file="$dir/$papertype-$date.pdf"
  link="$dir/$papertype.pdf"

  # Don't download the same file twice in a row.
  if [ -e "$file" ]
    then
    return
  fi

  mkdir -p "$dir"
  wget -O "$file" "$url"
  (
    cd $dir
    md5sum "$papertype-$date.pdf" > "$papertype-$date.pdf.md5"
  )

  md5a="`cut -d \  -f 1 $file.md5`"

  if [ -h $link ]
    then
    linkmd5="`readlink $link.md5`"
    md5b="`cut -d \  -f 1 $linkmd5`"
  fi

  if [ -h $link ] && [ "$md5a" = "$md5b" ]
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

