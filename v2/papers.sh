#!/bin/sh

paper() {
  set -e

  USAGE="usage: $0 --permit [permit number] --url [url] --papertype [public_notice or drawings] --date [like 2012-04-01]"

  while [ $# -gt 0 ]
  do
      case "$1" in
          --papertype) papertype="$2" && shift;;
          --url) url="$2" && shift;;
          --permit) permit="$2" && shift;;
          --date) date="$2" && shift;;
          -*) echo >&2 $USAGE
              exit 1;;
          *)  break;;
      esac
      shift
  done

  dir="pdfs/$permit"
  file="$dir/$papertype-$date.pdf"
  link="$dir/$papertype.pdf"

  # Don't download the file if I've already downloaded it today.
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

