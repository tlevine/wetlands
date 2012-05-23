from dumptruck import DumpTruck
from bucketwheel import * # Sorry

class RegulatoryPage(BucketMold):
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def load(self):
        raise NotImplementedError('You need to implement the load function for this bucket')

    def parse(self, text):
        raise NotImplementedError('You need to implement the load function for this bucket')


excavate([RegulatoryPage(
  url = 'http://www.mvn.usace.army.mil'
  '/ops/regulatory/publicnotices.asp?ShowLocationOrder=False'
)])
