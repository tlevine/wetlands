from time import sleep
import datetime
from dumptruck import DumpTruck
import demjson

dt = DumpTruck(
    dbname = 'wetlands.sqlite',
    auto_commit = False
)

def log(text):
    print(text)

class Bag:
    "A fancier stack, at some point"
    def __init__(self, buckets = [], table_name = '_bag'):
        self._table_name = table_name

        # So we can initialize them
        self.buckets = {Bucket.bucket: Bucket for Bucket in buckets}

        # Set up hierarchical relationships
        for bucketname, bucket in self.buckets.items():
            if bucket.motherbucket == None:
                dt.execute('''
CREATE TABLE IF NOT EXISTS `{bucket}` (
  scraper_run DATE NOT NULL,
  kwargs JSON NOT NULL,
  motherkwargs JSON,
  UNIQUE(scraper_run, kwargs)
) '''.format(bucket= bucket.bucket))
            else:
                dt.execute('''
CREATE TABLE IF NOT EXISTS `{bucket}` (
  scraper_run DATE NOT NULL,
  kwargs JSON NOT NULL,
  motherkwargs JSON NOT NULL,
  UNIQUE(scraper_run, kwargs),
  FOREIGN KEY(motherkwargs) REFERENCES `{motherbucket}`(`kwargs`)
) '''.format(bucket= bucket.bucket, motherbucket= bucket.motherbucket))

        # The bag table
        dt.execute('''
CREATE TABLE IF NOT EXISTS `%s` (
  pk INTEGER PRIMARY KEY,
  Bucket TEXT NOT NULL,
  MotherBucket TEXT,
  kwargs JSON NOT NULL
 )''' % self._table_name)

    def add(self, element):
        dt.insert({
            u'Bucket': element.bucket,
            u'MotherBucket': element.motherbucket,
            u'kwargs': element.kwargs,
        }, self._table_name)

    def pop(self):
        sql1 = 'SELECT pk, Bucket, MotherBucket, kwargs FROM `%s` LIMIT 1' % self._table_name
        results = dt.execute(sql1)
        if len(results) == 0:
            return None
        else:
            bucket_params = results[0]
            sql2 = 'DELETE FROM `%s` WHERE pk = %d' % (self._table_name, bucket_params['pk'])
            dt.execute(sql2)
            return self.buckets[bucket_params[u'Bucket']](**bucket_params['kwargs'])

class BucketMold:
    "The base getter scraper class"
    bucket = 'BucketMold'
    motherbucket = None

    def __init__(self, motherkwargs = None, **kwargs):
        self.kwargs = kwargs
        self.motherkwargs = motherkwargs

    def load(self):
        raise NotImplementedError('You need to implement the load function for this bucket')

    def parse(self, text):
        raise NotImplementedError('You need to implement the parse function for this bucket')

    def _go(self):
        log('')
        log('-------------------------------------------')
        log('')
        log('Loading this %s:' % self.bucket)
        log(demjson.encode(self.kwargs, compactly = False))
        blob = self.load()

        log('Parsing the bucket')
        childbuckets = self.parse(blob)
        if childbuckets == None:
            childbuckets = []

        log('Linking to its children')
        # That's what this loop does
        reference = {'scraper_run': scraper_run, 'motherkwargs': self.kwargs}
        for cb in childbuckets:
            kin = {'kwargs': cb.kwargs}
            kin.update(reference)
            dt.insert(kin, cb.bucket)

        # The first entry has no ancestors, so it has to make its own entry.
        if self.motherbucket == None:
            dt.insert({'scraper_run': scraper_run, 'kwargs': self.kwargs}, self.bucket)
        return childbuckets

    def reference(self):
        # For linking scraped data to this row
        return {
            'kwargs': self.kwargs,
            'motherkwargs': self.motherkwargs,
            'scraper_run': scraper_run
        }

try:
    scraper_run = dt.get_var('scraper_run')
except:
    scraper_run = datetime.date.today().isoformat()
    dt.save_var('scraper_run', scraper_run)

def excavate(bucketclasses = [], startingbuckets = []):
    "Start everything."

    # Bucket classes (page types)
    if bucketclasses == []:
        for g in globals().values():
            if isinstance(g, BucketMold) and g != BucketMold:
                bucketclasses.append(g)
    bag = Bag(buckets = bucketclasses)

    # The seed buckets
    if dt.execute('select count(*) as "c" from `%s`' % bag._table_name)[0]['c'] == 0:
        for b in startingbuckets:
            bag.add(b)

    # Go
    while True:
        currentbucket = bag.pop()

        if currentbucket == None:
            break

        for newbucket in currentbucket._go():
            bag.add(newbucket)

        log("Committing")
        # Commit at the end in case of errors.
        dt.commit()

        log("Taking a break") # Don't thrash the server
        sleep(3)

dt.drop('_dumptruckvars') # Hack to refresh the scraper_run
