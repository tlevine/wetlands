'''
Tests for combining new data with an existing fat.db
'''
import os
import json
from dumptruck import DumpTruck

class TestExtend:
    'Extend the database given new data.'
    dbfile = '/tmp/wetlands-test-dbfile'

    def setup(self):
        if os.path.exists(self.dbfile):
            os.remove(self.dbfile)

    def _load_fixture_sql(self, fixture_sql_file):
        'Create the cache database from a fixture SQL file.'
        os.system('sqlite3 "%s" < "%s"' % (self.dbfile, fixture_sql_file))

    def _rowcount_should_be(self, expected_rowcount):
        dt = DumpTruck(dbname = self.dbfile)
        observed_rowcount = dt.execute('select count(*) from `fat`')['count(*)']
        n.assert_equal(observed_rowcount, expected__rowcount)

    def _diff(self, test_name, expected_rowcount):
        self._load_fixture_sql(test_name + '.sql')
        dt = DumpTruck(dbname = self.dbfile)
        newdata = json.loads(open(test_name + '.json').read())
        dt.upsert(newdata)
        self._rowcount_should_be(expected_rowcount)

    def test_same(self):
        'When the new data are the same as the old data, no new data should be added.'
        self._diff('test_same', 44)

    def test_subset(self):
        'When the new data are a subset of the old data, no rows should be added.'
        self._diff('test_same', 164)

    def test_intersection(self):
        'When the new data contain some new rows and some old rows, new rows should be added.'
        self._diff('test_same', 168)

    def test_disjoint(self):
        'When the new data contain no old rows, new rows should be added.'
        self._diff('test_same', 208)
