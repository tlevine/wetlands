'''
Tests of commands that should fail
'''
import nose.tools as n

import build

class ParseFail:
    def test_fail(self):
        with n.assertRaises(ValueError):
            build.parse(self.listings_dir, self.pdfs_dir, self.data_dir)

class TestParseCacheNonmatchingListings(ParseFail):
    'Parse given a cache that doesn\'t match the listings directory.'
    @classmethod
    def setup_class(self):
        self.listings_dir = 'fixtures/listings-nonmatching'
        self.pdfs_dir = 'fixtures/pdfs'
        self.data_dir = 'fixtures/data'

class TestCacheNonmatchingPdfs(ParseFail):
    'Parse given a cache that doesn\'t match the pdfs directory.'
    @classmethod
    def setup_class(self):
        self.listings_dir = 'fixtures/listings'
        self.pdfs_dir = 'fixtures/pdfs-nonmatching'
        self.data_dir = 'fixtures/data'

class TestNoListings(ParseFail):
    'Parse given no listings. This should error.'
    @classmethod
    def setup_class(self):
        os.mkdir('/tmp/wetlands_test_build-listings')
        self.listings_dir = '/tmp/wetlands_test_build-listings'
        self.pdfs_dir = 'fixtures/pdfs'
        self.data_dir = '/tmp/wetlands_test_build-data'

