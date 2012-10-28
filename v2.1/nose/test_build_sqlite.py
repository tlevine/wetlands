import os
import nose.tools as n

import build

class CheckSqlite:
    def test_existance(self):
        'The fat.db file should be there.'
        n.assert_true(os.path.exists(os.path.join(self.data_dir, 'fat.db')))

class TestParseOneEmptyOneNotThere(CheckSqlite):
    'Parse given one empty directory and one that doesn\'t exist.'
    @classmethod
    def setup_class(self):
        for subdir in ['listings', 'data']:
            new = '/tmp/wetlands_test_build-' + subdir
            if not os.path.exists(new):
                os.mkdir(new)
        self.listings_dir = '/tmp/wetlands_test_build-listings'
        self.pdfs_dir = '/tmp/wetlands_test_build-pdfs'
        self.data_dir = '/tmp/wetlands_test_build-data'
        build.parse(self.listings_dir, self.pdfs_dir, self.data_dir)

class ParseEmpty:
    'Parse given empty directories.'
    @classmethod
    def setup_class(self):
        for subdir in ['listings', 'pdfs', 'data']:
            os.mkdir('/tmp/wetlands_test_build-' + subdir)
        self.listings_dir = '/tmp/wetlands_test_build-listings'
        self.pdfs_dir = '/tmp/wetlands_test_build-pdfs'
        self.data_dir = '/tmp/wetlands_test_build-data'
        build.parse(self.listings_dir, self.pdfs_dir, self.data_dir)

class ParseStandard:
    'Parse given a standard filesystem.'
    @classmethod
    def setup_class(self):
        self.listings_dir = 'fixtures/listings'
        self.pdfs_dir = 'fixtures/pdfs'
        self.data_dir = '/tmp/wetlands_test_build-data'
        build.parse(self.listings_dir, self.pdfs_dir, self.data_dir)

class ParseNoPdf:
    'Parse given a non-existant pdf directory. This should be fine.'
    @classmethod
    def setup_class(self):
        os.mkdir('/tmp/wetlands_test_build-pdfs')
        self.listings_dir = 'fixtures/listings'
        self.pdfs_dir = '/tmp/wetlands_test_build-pdfs'
        self.data_dir = '/tmp/wetlands_test_build-data'
        build.parse(self.listings_dir, self.pdfs_dir, self.data_dir)

class ParseCache:
    'Parse given a cache.'
    @classmethod
    def setup_class(self):
        self.listings_dir = 'fixtures/listings'
        self.pdfs_dir = 'fixtures/pdfs'
        self.data_dir = 'fixtures/data'
        build.parse(self.listings_dir, self.pdfs_dir, self.data_dir)
