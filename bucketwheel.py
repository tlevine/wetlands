from dumptruck import DumpTruck

dt = DumpTruck(
    dbname = 'wetlands.sqlite',
    auto_commit = False
)

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
  kwargs JSON,
  UNIQUE(kwargs)
) '''.format(bucket= bucket.bucket))
            else:
                dt.execute('''
CREATE TABLE IF NOT EXISTS `{bucket}` (
  kwargs JSON,
  motherkwargs JSON,
  UNIQUE(kwargs),
  FOREIGN KEY(motherkwargs) REFERENCES `{motherbucket}`(`kwargs`)
) '''.format(bucket= bucket.bucket, motherbucket= bucket.motherbucket))

        # The bag table
        dt.execute('''
CREATE TABLE IF NOT EXISTS `%s` (
  pk INTEGER PRIMARY KEY,
  Bucket TEXT,
  MotherBucket TEXT,
  kwargs JSON
 )''' % self._table_name)

    def add(self, element):
        dt.insert({
            u'Bucket': element.bucket,
            u'MotherBucket': element.motherbucket,
            u'kwargs': element.kwargs,
        }, self._table_name)

    def pop(self):
        sql1 = 'SELECT * FROM `%s` LIMIT 1' % self._table_name
        results = dt.execute(sql1)
        if len(results) == 0:
            return None
        else:
            bucket_params = results[0]
            sql2 = 'DELETE FROM `%s` WHERE pk = %d' % (self._table_name, bucket_params['pk'])
            dt.execute(sql2)
            return self.buckets[bucket_params['Bucket']](**bucket_params['kwargs'])

class BucketMold:
    "The base getter scraper class"
    bucket = 'Bucket'
    motherbucket = None

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def load(self):
        raise NotImplementedError('You need to implement the load function for this bucket')

    def parse(self, text):
        raise NotImplementedError('You need to implement the load function for this bucket')

    def go(self):
        blob = self.load()
        childbuckets = self.parse(textblob)
        ancestry = [{'kwargs': cb.kwargs, 'motherkwargs': self.kwargs} for cb in childbuckets]
        dt.insert(ancestry, self.bucket)
        return morepages

def excavate(startingbuckets = [], bucketclasses = []):
    "Start everything."

    # Bucket classes (page types)
    if bucketclasses == []:
        for g in globals().values():
            if isinstance(g, BucketMold) and g != BucketMold:
                bucketclasses.append(g)
    bag = Bag(buckets = bucketclasses)

    # The seed buckets
    for b in startingbuckets:
        bag.add(b)

    # Go
    while True:
        currentbucket = bag.pop()

        if currentbucket == None:
            break

        for newbucket in currentbucket.go():
            bag.add(newbucket)

        # Commit at the end in case of errors.
        dt.commit()

