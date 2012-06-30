Army Corps 404 Website Scraper, version 1
=======
The data
---------

We are scraping [this website](http://www.mvn.usace.army.mil/ops/regulatory/publicnotices.asp?ShowLocationOrder=False).

You can see example files from the website in the `listing.example`
and `pdf.example` directories; the program puts corresponding data
into the `listing` and `pdf` directories.

The program
---------

Raw downloads are stored in three (!) different places: the filesystem,
the `raw_files` table in the database and in proper database tables.

### Filesystem

Raw data are stored in the directories `listing` and `pdf`.
`listing` is for [this web page](http://www.mvn.usace.army.mil/ops/regulatory/publicnotices.asp?ShowLocationOrder=False),
and `pdf` is for the pdf files. Here is the structure of these directories.

    ./
      listing/
        2012-05-22.html
        2012-05-23.html
      pdf/
        MVN-2002-3090-EFF/
          2012-05-22/
            FINAL-JPN.pdf
            PLats.pdf
          2012-05-23/
            FINAL-JPN.pdf
            PLats.pdf
        MVN-2012-1189-EOO/
          2012-05-23/
            1189.pdf
            sec10PN_1189.pdf

### raw_files database table

The filesystem structure is convenient to access, but managing versions
of the files is a little easier in a database. The `raw_files` table
is similarly simple to a table; here is the schema.

    CREATE TABLE IF NOT EXISTS raw_files (
      scraper_run DATE NOT NULL,
      Bucket TEXT NOT NULL,
      kwargs JSON NOT NULL,
      url TEXT NOT NULL,

      datetime_scraped DATETIME NOT NULL,
      raw BASE64 TEXT NOT NULL,

      UNIQUE(scraper_run, Bucket, kwargs)
      UNIQUE(scraper_run, url)
    )

`kwargs` is the paramaters to the document retrieval and parse function;
is used as a main identifier to link different scraped documents.
The field `url` also works as an identifier.
`scraper_run` is the day on which the script was started, but
`datetime_scraped` includes the time when the particular document was
downloaded. The document is stored base64-encoded in `raw`.

I didn't need to use kwargs thing because this site's HTTP requests
are all ordinary GET requests, but it'll help when we want to do more
processing offline later because it'll let me use the same queue.

### Proper database tables

Scraped data stored across various tables which are set up to allow
for easy maintanance, searching and analysis of links among data,
time-based searches, scraped data and metadata.

The raw files are stored in these same tables in addition to the
`raw_files` table. They are also parsed and linked together.

    Explain the schema here.

The data will quickly become too big for git, so they are not versioned
in git; we need to come up with some other way of handling backups
and distribution (probably rsync and bittorrent).

Architecture
---------

The program uses a simple message queue (actually more like a mosh pit)
called Bucket Wheel that runs atop
SQLite. The queue makes writing the scraper convenient,
but it is not threadsafe, just so you know.

Tables are mapped to Python classes, one class for each type of document.
This is not done properly with meta classes, so setting this up
involves a few hacks.

Loading and parsing of each particular document is handled

And **do not run two instances of this in the same environment**;
that will mess up the queue.


### Size

I ran this on May 23, 2012 and wound up with with 100 megabytes
of pdf downloads and a 268-megabyte database. (Those 268 megabytes
include two copies of each download plus metadata and several
reformatted versions.) We won't hit filesystem limits for a while,
but the database might start to get slow soon; if we add 300 megabytes
to the database each day, we can expect it to reach 100 gigabytes in a year.

A simple solution would be run the database in RAM (which I have 16
gigabytes of) and split it up into monthly or weekly subsets, which
might make backups easier anyway.
