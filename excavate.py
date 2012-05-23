from dumptruck import DumpTruck
from bucketwheel import * # Sorry

class Get(BucketMold):
    bucket = 'Get'
    def load(self):
        pass

class RegulatoryPage(BucketMold):
    bucket = 'RegulatoryPage'
    def load(self):
        self.kwargs['url']
        raise NotImplementedError('You need to implement the load function for this bucket')

    def parse(self, text):
        raise NotImplementedError('You need to implement the load function for this bucket')

class PdfDownload(BucketMold):
    bucket = 'PdfDownload'


dt.execute('''
CREATE TABLE IF NOT EXISTS raw_files (
  scraper_run DATE NOT NULL,
  Bucket TEXT NOT NULL,
  kwargs JSON NOT NULL,

  datetime_scraped DATETIME NOT NULL,
  raw BLOB NOT NULL,

  UNIQUE(scraper_run, Bucket, kwargs)
)''')
excavate(
  startingbuckets = [RegulatoryPage(
    url = 'http://www.mvn.usace.army.mil'
    '/ops/regulatory/publicnotices.asp?ShowLocationOrder=False'
  )],
  bucketclasses = [RegulatoryPage]
)
