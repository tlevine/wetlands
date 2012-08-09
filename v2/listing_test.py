import os
import unittest
import datetime
import json
import pymongo
from listing import \
     listing_retrieve, listing_parse, listing_save, \
    _clean_permit_application_number, \
    _clean_mvn_permit_application_number

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
            'publicNoticeDate': datetime.datetime,
            'expirationDate': datetime.datetime,
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

class TestListingSave(unittest.TestCase):
    def setUp(self):
        self.connection = pymongo.Connection('localhost')
        self.db = self.connection.wetlands_test

        listingData = open(os.path.join('fixtures', 'listing.json'))
        self.data = json.loads(listingData.read())

    def test_save_first(self):
        self.db.permits.drop()
        listing_save(self.data, self.db)
        self.db.permit.find_one()

    def test_save_again(self):
        os.system('mongorestore -d wetlands_test fixtures/listing_dump/wetlands_test')
        listing_save(self.data, self.db)
        self.db.permit.find_one()

class TestMVNPermitApplicationNumberConversion(unittest.TestCase):
    'Permit application numbers should get cleaned up, or I should see errors.'

    def _p(self, permit_application_number, should = None):
        'Does the cleaning happen properly?'

        if should == None:
            should = permit_application_number

        self.assertEqual(
            _clean_mvn_permit_application_number(permit_application_number),
            should
        )

    def _r(self, permit_application_number, raises = AssertionError):
        'Does the cleaning raise an error?'
        with self.assertRaises(raises):
            _clean_mvn_permit_application_number(permit_application_number)

    def test_clean_short(self):
        self._p("MVN-2012-00926")

    def test_clean_long(self):
        self._p("MVN-2012-01027-WMM")

    def test_space1_long(self):
        self._p("MVN 2010-1270-WII", should = "MVN-2010-1270-WII")

    def test_space2_long(self):
        self._p("MVN-2010 1270-WII", should = "MVN-2010-1270-WII")

    def test_space3_long(self):
        self._p("MVN-2010-1270 WII", should = "MVN-2010-1270-WII")

    def test_space1_space3_long(self):
        self._p("MVN 2010-1270 WII", should = "MVN-2010-1270-WII")

    def test_weirdspace_space1_long(self):
        self._p("MVN 2006-0335-CY A", should = "MVN-2006-0335-CYA")

    def test_weirdspace_long(self):
        self._p("MVN-2006-0335-CY A", should = "MVN-2006-0335-CYA")

    def test_bad_first_block_long(self):
        self._r("ABC-2012-01027-WMM")

    def test_old_year_second_block(self):
        self._p("MVN-1987-01027-WMM")

    def test_strange_year_second_block(self):
        self._r("MVN-1887-01027-WMM")

    def test_nonletters_in_fourth_block(self):
        self._r("MVN-2012-01027-W3M")

    def test_fourth_block_length(self):
        self._p("MVN-2012-0000-ABCD")

    def test_second_block_length(self):
        self._r("MVN-02012-0000-ABC")

    def test_short_fourth_block(self):
        self._p('MVN-2012-01053-CJ')

if __name__ == "__main__":
    unittest.main()
