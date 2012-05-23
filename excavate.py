from dumptruck import DumpTruck
from bucketwheel import * # Sorry

class Get(BucketMold):
    bucket = 'Get'
    def load(self):

class RegulatoryPage(BucketMold):
    bucket = 'RegulatoryPage'
    def load(self):
        self.kwargs['url']
        raise NotImplementedError('You need to implement the load function for this bucket')

    def parse(self, text):
        raise NotImplementedError('You need to implement the load function for this bucket')

class PdfDownload(BucketMold):
    bucket = 'PdfDownload'

excavate(
  startingbuckets = [RegulatoryPage(
    url = 'http://www.mvn.usace.army.mil'
    '/ops/regulatory/publicnotices.asp?ShowLocationOrder=False'
  )],
  bucketclasses = [RegulatoryPage]
)
