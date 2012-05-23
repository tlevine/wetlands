Army Corps 404 Website Scraper
=======

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

Raw data are stored in the directories `listing` and `pdf`. Here is
their structure.

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

Scraped data stored across various tables which are set up to allow
for easy maintanance, searching and analysis of links among data,
time-based searches, scraped data and metadata.

The raw files are stored in these same tables



They are then parsed and linked together inside of the database.

    Explain the schema here.

The data will quickly become too big for git, so they are not versioned
in git; we need to come up with some other way of handling backups.

directories `listing` (for the web page) and `pdf` for the pdf files

The program architecture uses a simple message queue running
on top of SQLite. The queue makes writing the scraper convenient,
but it is not threadsafe, just so you know.