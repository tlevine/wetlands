import os
from dumptruck import DumpTruck
from urllib2 import urlopen, URLError
from bucketwheel import * # Sorry

from lxml.html import fromstring

RETRIES = 5
WAIT = 3 # seconds, raised to the retry

class Get(BucketMold):
    bucket = 'Get'
    bash = None
    def load(self):
        url = self.kwargs['url']

        # Database save
        for retry in range(1, 1 + RETRIES):
            try:
                raw = urlopen(url).read()
            except URLError:
                sleep(WAIT**RETRIES)

        dt.insert({
            'scraper_run': scraper_run,
            'Bucket': self.bucket,
            'kwargs': self.kwargs,
            'url': url,
            'datetime_scraped': datetime.datetime.now(),
            'raw': raw
        })

        # Filesystem save (inefficient but convenient)
        os.system(bash % {'url': url})

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
        RRRaise(AssertionError('Not exactly one node'))
    else:
        return nodes[0]

class Listing(GET):
    bucket = 'Listing'
    motherbucket = None
    bash = """
mkdir -p listing
cd listing
curl %(url)s > """ + scraper_run + '.html'

    NCOL = 8
    COLNAMES = (
        'Project Description',
        'Applicant',
        'Public Notice Date',
        'Expiration Date',
        'Permit Application No.',
        'View or Download',
        'Location',
        'Project Manager'
    )

    @staticmethod
    def parsedate(rawdate):
        return datetime.datetime.strptime(rawdate, '%m/%d/%Y').date()

    def parse(self, rawtext):
        # There are more data in the comments!
        text_with_locations = rawtext.replace('<!--', '').replace('-->', '').replace('&nbsp;', ' ')

        html = fromstring(text_with_locations)
        table = onenode(html, '//table[@width="570" and @border="1" and @cellpadding="0" and @cellspacing="0" and @bordercolor="#ffffff" and @bgcolor="#efefef"')
        trs = table.xpath('tr')

        # Getting the cells 
        thead = [td.text_content().strip() for td in trs.pop(0)]
        if len(thead) != self.NCOL:
            RRRaise(AssertionError('The table header does not have exactly %d cells.' % self.NCOL)

        if thead != self.COLNAMES:
            RRRaise(AssertionError('The table header does not have the right names.')

        # List of dictionaries of data
        data = []
        for tr in trs:
            if len(tr.xpath('td')) != self.NCOL:
                RRRaise(AssertionError('The table row does not have exactly %d cells.' % self.NCOL)

            # As a dict
            row = dict(zip(thead, [td.text_content().strip() for td in tr.xpath('td')]))

            # Dates
            row['Public Notice Date'] = self.parsedate(row['Public Notice Date'])
            row['Expiration Date'] = self.parsedate(row['Expiration Date'])

            # PDF download links
            pdfkeys = set(tr.cssselect('td/a/text()'))
            if pdfkeys.issubset({'Public Notice', 'Drawings'}):
                RRRaise(AssertionError('The has unexpected hyperlinks.')
            if len(pdfkeys) == 0:
                RRRaise(AssertionError('No pdf hyperlinks found.')

            for key in ['Public Notice', 'Drawings']:
                row[key] = onenode(tr, 'td/a[text()="%s"]/@href' % key)
                if row[key][:4] != 'pdf/':
                    RRRaise(AssertionError('The %s pdf link doesn\'t have the expected path.' % key))

        # Now clean them.
        for row in body:
            dict(zip(header, 

        raise NotImplementedError('You need to implement the load function for this bucket')

class PdfDownload(BucketMold):
    bucket = 'PdfDownload'
    motherbucket = 'Listing'
    bash = "mkdir -p pdf; cd pdf; wget '%(url)s'"

    def parse(self, text):
        raise NotImplementedError('You need to implement the load function for this bucket')

dt.execute('''
CREATE TABLE IF NOT EXISTS raw_files (
  scraper_run DATE NOT NULL,
  Bucket TEXT NOT NULL,
  kwargs JSON NOT NULL,
  url TEXT NOT NULL,

  datetime_scraped DATETIME NOT NULL,
  raw BLOB NOT NULL,

  UNIQUE(scraper_run, Bucket, kwargs)
  UNIQUE(scraper_run, Bucket, url)
)''')
excavate(
  startingbuckets = [RegulatoryPage(
    url = 'http://www.mvn.usace.army.mil'
    '/ops/regulatory/publicnotices.asp?ShowLocationOrder=False'
  )],
  bucketclasses = [RegulatoryPage]
)
