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
        raise ValueError('Not exactly one node')
    else:
        return nodes[0]

class Listing(GET):

    bucket = 'Listing'
    motherbucket = None
    bash = """
mkdir -p listing
cd listing
curl %(url)s > """ + scraper_run + '.html'

    def parse(self, rawtext):
        # There are more data in the comments!
        text_with_locations = rawtext.replace('<!--', '').replace('-->', '')

        html = fromstring(text_with_locations)
        table = onenode(html, '//table[@width="570" and @border="1" and @cellpadding="0" and @cellspacing="0" and @bordercolor="#ffffff" and @bgcolor="#efefef"')
        trs = table.xpath('tr')

        header = [td.text_content().strip() for td in trs.pop(0)]
        if len(header) != 

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
