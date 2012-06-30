#!/bin/sh

papers() {
  # Parametrize this.
  permit=MVN-a93409234
  date=2012-06-01
  papertype=public_notice
  url=localhost:5678/thuho.pdf
  file="pdfs/$permit/$papertype-$date.pdf"

  wget -O "$file" "$url"
  md5sum "$file" > "$file.md5"
}
