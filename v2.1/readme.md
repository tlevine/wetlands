Army 404 Scraper v2.1
======
I study data from the Army 404 website in three steps.

  1. **Download** listing pages, public notices and drawings to the hard drive.
  2. **Build** sqlite3, json and csv based on the files saved above.
  3. **Serve** a website with this information.

## Download

This downloads new data.

    . activate
    download

<!-- Add documentation from the v2 -->

## Build

This builds the databases.

    . activate
    build

### Construction process
It opens the files contained in `listings` and `pdfs` and then generates two
tables (fat and skinny) in three formats (sqlite3, json and csv), for a total
of six files. They are saved in `data`.

In each of these files, one row represents a single permit application. In the
sqlite3 and csv formats, non-tabular data are represented as json stored in a
table cell. The fat version has more columns.

### Caching
The fat sqlite3 database is generated first and then converted to the other
formats. It contains some data about the run that the others don't. If
`data/fat.db` already exists, the build script checks for these other data and
skips things that have already been built.

The extra data that the fat sqlite3 database contains are lists of listings
files that have been parsed. Based on this and the main table, the build script
is can tell what has already been processed and avoid processing it.

The cache doesn't work if you've changed the schema; delete `data/fat.db` if
that happens.

## Serve

Serve the website like so.

    . activate
    serve

The website is served from the root of the git repository, so you can also
just check out the git repository to a web server, setting the root of the
website to the git repository's working directory.

### Editing the website
