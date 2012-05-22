from dumptruck import DumpTruck

dt = DumpTruck(
    dbname = 'wetlands.sqlite',
    auto_commit = False
)

class Bag:
    "A fancier stack, at some point"
    def __init__(self, startingstack = [], table_name = '_bag'):
        self._table_name = table_name
        dt.create_table({
            'Bucket': 'Bucket',
            'MotherBucket': 'MotherBucket',
            '__init__': [[], {}],
        }, self._table_name, if_not_exists = True)
        try:
            assert self.__len__() > 0
        except:
            for element in startingstack:
                self.add(element)

    def add(self, element):
        dt.insert({
            'Bucket': element.bucket,
            'MotherBucket': element.motherbucket,
            '__init__': element.init_params,
        }, self._table_name)

    def pop(self):
        results = dt.execute('SELECT * FROM `%s` LIMIT 1' % self._table_name)
        if len(results) == 0:
            pass

class Bucket:
    "The base getter scraper class"
    def go(self):
        textblob = self.load()
        morepages = self.parse(textblob)
        return morepages

def seed(stacklist):
    "Start everything."
    stack = Stack(stacklist)

    while len(stack) > 0:
        try:
            add_to_stack = stack.last().go()
        except Exception:
            raise
        else:
            stack.pop()
            if add_to_stack != None:
                stack.extend(add_to_stack)

# --------------------------------------------------
# End Bucket-Wheel
# --------------------------------------------------

URLS={
  "main":"http://www.nedbank.co.za/website/content/map/branches.asp"
, "suburbs-base":"http://www.nedbank.co.za/website/content/map/getSuburbs.asp?q="
, "cities-base":"http://www.nedbank.co.za/website/content/map/getData.asp?q="
}

class Get(Bucket):
    def __init__(self, url):
        self.url = url

    def load(self):
        randomsleep()
        return requests.get(self.url).text

class Menu(Get):
    "Returns provinces"
    def parse(self, text):
        x=fromstring(text)
        provinces=options(x.xpath('id("province")')[0],valuename="provinceId",textname="provinceName",ignore_value="0")
        for province in provinces:
            province['provinceUrl'] = URLS['suburbs-base'] + province['provinceId']
            province['scraperrun'] = scraperrun

        save(['provinceUrl', 'scraperrun'], provinces, 'provinces')
        return [Province(p['provinceUrl']) for p in provinces]
