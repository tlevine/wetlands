#!/bin/sh

papers() {
  # Parametrize this.
  permit=MVN-a93409234
  date=2012-06-01
  papertype=public_notice
  url=localhost:5678/thuho.pdf
  file="pdfs/$permit/$papertype-$date.pdf"
  link="pdfs/$permit/$papertype.pdf"

  wget -O "$file" "$url"
  md5sum "$file" > "$file.md5"

  if [ -e $link && `cut -d \  -f 1 $file.md5` = `cut -d \  -f 1 $link.md5` ]
    then
    # If this is the same as the previous file,

    # delete the current file
    rm "$file" "$file.md5"

    # and update the "last seen" field in the database.
    # mongo wetlands --eval "db.permits"

  else
    # If it's different or new, change the links
    rm "$link" "$link.md5"
    ln -s "$file" "$link"
    ln -s "$file.md5" "$link.md5"

    # and update the "last seen" and "md5sum" fields in the database.
    # mongo wetlands --eval "db.permits"

  fi
}

