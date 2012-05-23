#!/usr/bin/env python2
import re
import os
import base64
from dumptruck import DumpTruck
import requests
from unidecode import unidecode
from lxml.html import fromstring, tostring
from time import sleep

from bucketwheel import * # Sorry

RETRIES = 4
WAIT = 2 # seconds, raised to the retry

class Get(BucketMold):
    bucket = 'Get'
    bash = None
    def load(self):
        url = self.kwargs['url']

#       # Database save
#       for retry in range(1, 1 + RETRIES):
#           try:
#               raw = urlopen(url, 'rb').read()
#           except URLError:
#               print('Retrying download of %s' % url)
#               sleep(WAIT**RETRIES)
#           else:
#               break
        print(url)
        raw = requests.get(url).content
        self.datetime_scraped = datetime.datetime.now()

        dt.insert({
            u'scraper_run': scraper_run,
            u'Bucket': self.bucket,
            u'kwargs': self.kwargs,
            u'url': url,
            u'datetime_scraped': self.datetime_scraped,
            u'raw': base64.b64encode(raw)
        }, 'raw_files')

        # Filesystem save (inefficient but convenient)
        os.system(self.bash % self.kwargs)

        return raw

QUIET = False

def RRRaise(exception):
    if QUIET:
        dt.insert({
            'exception': str(type(exception)),
            'message': str(exception),
            'datetime': datetime.datetime.now(),
            'scraper_run': scraper_run
        }, 'exceptions')
    else:
        raise exception

def onenode(html, xpath):
    nodes = html.xpath(xpath)
    if len(nodes) != 1:
        print(map(tostring, nodes))
        RRRaise(AssertionError('Not exactly one node'))
    else:
        return nodes[0]

class Listing(Get):
    bucket = 'Listing'
    motherbucket = None
    bash = "mkdir -p listing; cd listing; curl %(url)s > `date --rfc-3339 date`.html"

    NCOL = 8
    COLNAMES = [
        'Project Description',
        'Applicant',
        'Public Notice Date',
        'Expiration Date',
#       'Permit Application No.',
        'PermitApplication No.',
        'View or Download',
        'Location',
        'Project Manager'
    ]
    PHONE_NUMBER = re.compile(r'[^0-9]*(\d{3}-\d{3}-\d{4})[^0-9]*')

    @staticmethod
    def parsedate(rawdate):
        return datetime.datetime.strptime(rawdate, '%m/%d/%Y').date()

    def parse(self, rawtext):
        # There are more data in the comments!
        text_with_locations = rawtext.replace('<!--', '').replace('-->', '').replace('&nbsp;', ' ')
        unicodetext = unidecode(text_with_locations)
        html = fromstring(unicodetext)
        table = onenode(html, '//table[@width="570" and @border="1" and @cellpadding="0" and @cellspacing="0" and @bordercolor="#ffffff" and @bgcolor="#efefef"]')
        trs = table.xpath('tr')

        # Getting the cells 
        thead = [td.text_content().strip() for td in trs.pop(0)]
        if len(thead) != self.NCOL:
            print(thead)
            RRRaise(AssertionError('The table header does not have exactly %d cells.' % self.NCOL))

        if thead != self.COLNAMES:
            pairs = zip(thead, self.COLNAMES)
            for a, b in pairs:
                print(a, b), 'Match' if a == b else 'Differ'
            RRRaise(AssertionError('The table header does not have the right names.'))

        # List of dictionaries of data
        data = []
        publicnotices = []
        drawings = []
        for tr in trs:
            if len(tr.xpath('td')) != self.NCOL:
                RRRaise(AssertionError('The table row does not have exactly %d cells.' % self.NCOL))

            # As a dict
            row = dict(zip(thead, [td.text_content().strip() for td in tr.xpath('td')]))

            # Dates
            row['Public Notice Date'] = self.parsedate(row['Public Notice Date'])
            row['Expiration Date'] = self.parsedate(row['Expiration Date'])

            # PDF download links
            del(row['View or Download'])
            pdfkeys = set(tr.xpath('td[position()=6]/descendant::a/text()'))
            if not pdfkeys.issubset({'Public Notice', 'Drawings'}):
                print(pdfkeys)
                RRRaise(AssertionError('The table row has unexpected hyperlinks.'))
            if len(pdfkeys) == 0:
                print row
                RRRaise(AssertionError('No pdf hyperlinks found for permit %s.' % row['PermitApplication No.']))
            for key in ['Public Notice', 'Drawings']:
                try:
                    row[key] = unicode(onenode(tr, 'td/descendant::a[text()="%s"]/@href' % key))
                except AssertionError:
                    if key == 'Public Notice':
                        raise
                    else:
                        continue

                if row[key][:4] != 'pdf/':
                    RRRaise(AssertionError('The %s pdf link doesn\'t have the expected path.' % key))

            # Project manager contact information
            del(row['Project Manager'])
            pm = onenode(tr, 'td[position()=8]')

            # Email address
            try:
                row['Project Manager Email'] = onenode(pm, 'descendant::a/@href')
            except AssertionError:
                print(row)
                raise

            if row['Project Manager Email'][:7] == 'mailto:':
                row['Project Manager Email'] = unicode(row['Project Manager Email'][7:])
            else:
                msg = 'This is a strange email link: <%s>' % row['Project Manager Email']
                RRRaise(AssertionError(msg))

            # Name 
            row['Project Manager Name'] = onenode(pm, 'descendant::a').text_content().strip()

            # Phone number
            phone_match = re.match(self.PHONE_NUMBER, pm.text_content())
            if phone_match:
                row['Project Manager Phone'] = phone_match.group(1)
            else:
                print(row)
                msg = 'This is a strange phone number: %s' % pm.text_content()
                RRRaise(AssertionError(msg))

            # References
            row['datetime_scraped'] = self.datetime_scraped
            row['kwargs'] = self.kwargs
            row['scraper_run'] = scraper_run

            # Append to our big lists
            data.append(row)
            cwd = 'http://www.mvn.usace.army.mil/ops/regulatory/'
            publicnotices.append(PublicNotice(
                url = cwd + row['Public Notice'],
                permit = row['PermitApplication No.']
            ))
            if row.has_key('Drawings'):
                drawings.append(Drawings(
                    url = cwd + row['Drawings'],
                    permit = row['PermitApplication No.']
                ))

        dt.insert(data, 'ListingData')
        return publicnotices + drawings

class PdfDownload(Get):
    motherbucket = 'Listing'
    bash = "mkdir -p 'pdf/%(permit)s'; cd 'pdf/%(permit)s'; wget '%(url)s'"

class PublicNotice(PdfDownload):
    bucket = 'PublicNotice'

    def parse(self, text):
        raise NotImplementedError('You need to implement the parse function for this bucket')

class Drawings(PdfDownload):
    bucket = 'Drawings'

    def parse(self, text):
        raise NotImplementedError('You need to implement the load function for this bucket')

# Store raw downloads in a table
dt.execute('''
CREATE TABLE IF NOT EXISTS raw_files (
  scraper_run DATE NOT NULL,
  Bucket TEXT NOT NULL,
  kwargs JSON NOT NULL,
  url TEXT NOT NULL,

  datetime_scraped DATETIME NOT NULL,
  raw BASE64 TEXT NOT NULL,

  UNIQUE(scraper_run, Bucket, kwargs)
  UNIQUE(scraper_run, Bucket, url)
)''')

# Data associated with the listing page
dt.execute('''
CREATE TABLE IF NOT EXISTS ListingData (
  scraper_run DATE NOT NULL,
  kwargs JSON NOT NULL,
  datetime_scraped DATETIME NOT NULL,
  
  [Project Description] TEXT NOT NULL,
  Applicant TEXT NOT NULL,
  [Public Notice Date] DATETIME NOT NULL,
  [Expiration Date] DATETIME NOT NULL,
  [PermitApplication No.] TEXT NOT NULL,
  [Public Notice] TEXT NOT NULL,
  [Drawings] TEXT,
  [Location] TEXT,
  [Project Manager Email] TEXT NOT NULL,
  [Project Manager Name] TEXT NOT NULL,
  [Project Manager Phone] TEXT NOT NULL,

  FOREIGN KEY(scraper_run, [PermitApplication No.])
    REFERENCES `Listing`(scraper_run, [PermitApplication No.]),
  UNIQUE(scraper_run, [PermitApplication No.]),
  UNIQUE([Public Notice]),
  UNIQUE(Drawings),
  UNIQUE([PermitApplication No.])
)''')


excavate(
  startingbuckets = [Listing(
    url = 'http://www.mvn.usace.army.mil'
    '/ops/regulatory/publicnotices.asp?ShowLocationOrder=False'
  )],
  bucketclasses = [Listing, PublicNotice, Drawings]
)
