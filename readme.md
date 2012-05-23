Army Corps 404 Website Scraper
=======

TODO

* Add pictures to the readme.
* Tell Scott about the readme.
* Document the schema, installing, running, &c.

Prospectus
-------------
There are many, many permits issued to fill and/or dredge wetlands in the New Orleans District, perhaps the most vulnerable district to wetland destruction in the United States.  And many project reviewers.  There may be 30 standard permits a week, and few advocates, whose time is overcommitted.  There are probably more general permits issued—these are never publicly noticed.  It takes a watchdog a minimum of 4 hours to review the 404 website for possible targets for comment, and 8 hours average for each comment.  Each FOIA takes an hour minimum.  Phone calls with regulators take 15 minutes to half an hour, usually. 

Once permits "fall off the page," a FOIA must be submitted to obtain documents that were once public.  Final Decision documents almost always require a FOIA.  It would be more productive to have to mail one FOIA.

Automated scrape would preserve these documents, and allow yearly review of impacts allowed by permitting. It would free up advocate time to investigate general permits hidden from public view, as well as follow up on decision documents and investigate permit violations—all of which are needed for effective watchdogging.    It would assist independent review of cumulative impacts, as required of the Army Corps by rule.

Additional services like OCR and text searches within the Public Notice could streamline permit review even more.  The Mississippi river Collaborative has recently proposed commenting on all permits 10 acres or more. In the New Orleans District, this will increase the work load substantially.  Any time saved in permit review, finding these 10 acre permits, is time better spent fighting bad permits, and analyzing the patterns of Corps regulatory to strategically fight wetlands destruction.  

Analysing and preventing wetlands destruction from the 404 process in the New Orleans District presents a challenge beyond that in most districts.  But if this program is successful, it can be applied to other Army Corps Districts around the nation.

The Army Corps, by federal rule, is required  to analyse permits for “Cumulative” impact of permitting, by using a “Watershed Approach.”

Holy Moly, but do they avoid doing this.  They do know how, but need encouragement.  Automation would assist them as well. 

Such a recordkeeping / databasing/ spreadsheet-making scraper software would aid in our pressure for the Corps to regard cumulative impacts of Permits.   It would also assist independent scientific review of impacts and mitigation. 

Thanks for whatever assistance you can give to our efforts to protect the wetlands that protect us.  Thanks for helping to keep us afloat. 

For a Healthy Gulf,

Scott


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
      UNIQUE(scraper_run, Bucket, url)
    )

`kwargs` is the paramaters to the document retrieval and parse function;
is used as a main identifier to link different scraped documents.
The field `url` is provided for convenience, but note that it does not
necessarily uniquely identify a document.
`scraper_run` is the day on which the script was started, but
`datetime_scraped` includes the time when the particular document was
downloaded. The document is stored base64-encoded in `raw`.


### Proper database tables

Scraped data stored across various tables which are set up to allow
for easy maintanance, searching and analysis of links among data,
time-based searches, scraped data and metadata.

The raw files are stored in these same tables in addition to the
`raw_files` table. They are also parsed and linked together.

    Explain the schema here.

The data will quickly become too big for git, so they are not versioned
in git; we need to come up with some other way of handling backups.

Architecture
---------

The program uses a simple message queue (`bucketwheel.py`) running
on top of SQLite. The queue makes writing the scraper convenient,
but it is not threadsafe, just so you know.

Tables are mapped to Python classes, one class for each type of document.
This is not done properly with meta classes, so setting this up
involves a few hacks.

Loading and parsing of each particular document is handled

But *do not run two instances of this in the same environment*;
that may mess up the data.


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
