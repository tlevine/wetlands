import os
from dumptruck import DumpTruck
from urllib2 import urlopen, URLError
from bucketwheel import * # Sorry

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
            'kwargs': self.kwargs
            'url': url,
            'datetime_scraped': datetime.datetime.now(),
            'raw': raw
        })

        # Filesystem save (inefficient but convenient)
        os.system(bash % {'url': url})

        return raw

class RegulatoryPage(GET):
    bucket = 'RegulatoryPage'
    bash = """
mkdir -p regulatorypage
cd regulatoypage
curl %(url)s > """ + scraper_run + '.html'

    def parse(self, text):
        raise NotImplementedError('You need to implement the load function for this bucket')

class PdfDownload(BucketMold):
    bucket = 'PdfDownload'
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
