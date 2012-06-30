import os
import unittest
import datetime
import json
from listing import listing_retrieve, listing_parse, listing_save

class TestListingParse(unittest.TestCase):
    def setUp(self):
        "Load HTML and expected JSON and parse the HTML."
        listing = open(os.path.join('fixtures', 'listing.html'))
        listingData = open(os.path.join('fixtures', 'listing.json'))

        self.html = listing.read()
        self.observedData = listing_parse(self.html)
        self.expectedData = json.loads(listingData.read())

        listing.close()
        listingData.close()

    def test_length(self):
        "The table should have 44 items."
        self.assertEqual(len(self.observedData), 44)

    def test_types(self):
        "The data should be of appropriate types."
        expectedTypes = {
            'projectDescription': unicode,
            'applicant': unicode,
            'location': unicode,
            'publicNoticeDate': datetime.date,
            'expirationDate': datetime.date,
            'permitApplicationNumber': unicode,
            'publicNoticeUrl': unicode,
            'drawingsUrl': unicode,
            'projectManagerEmail': unicode,
            'projectManagerName': unicode,
            'projectManagerPhone': unicode,
        }
        self.maxDiff = None
        observedTypes = {k: type(v) for k, v in self.observedData[0].items()}
        self.assertDictEqual(observedTypes, expectedTypes)

    def test_keys(self):
        "The data should have the appropriate keys."
        observed = set(self.observedData[0].keys())
        expected = {
#           'scriptRuns', # List of datetimes when run
            'location',
            'projectDescription',
            'applicant',
            'publicNoticeDate',
            'expirationDate',
            'permitApplicationNumber',
            'publicNoticeUrl',
            'drawingsUrl',
            'projectManagerEmail',
            'projectManagerName',
            'projectManagerPhone',
        }
        self.assertSetEqual(observed, expected)

#   def test_data(self):
#       "The observed data should equal the expected data."
#       self.assertListEqual(self.observedData, self.expectedData)

class TestListingRetrieve(unittest.TestCase):
    def setUp(self):
        self.observedHtml = listing_retrieve(url="http://localhost:5678/listing.html", stamp='test')
        self.expectedHtml = open('fixtures/listing.html').read()

    def test_output(self):
        self.assertEqual(self.observedHtml, self.expectedHtml)

    def test_file(self):
        self.assertEqual(open('listings/test.html').read(), self.expectedHtml)

    def tearDown(self):
        os.remove('listings/test.html')

#class TestListingSave(unittest.TestCase):
#    def setUp(self):
#        "Load expected JSON."
#        listingData = open(os.path.join('fixtures', 'listing.json'))
#        self.data = json.loads(listingData.read())
#        listingData.close()

#        self.connection = pymongo.Connection('desk')
#        self.db = self.connection.wetlands_test

#    def test_save(self):
#        listing_save(self.data, self.db)
#        self.db.find

if __name__ == "__main__":
    unittest.main()
