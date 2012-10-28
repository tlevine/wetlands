'''
Tests of commands that should fail
'''
import os
import nose.tools as n

import build

class ParseFail:
    def test_fail(self):
        with n.assert_raises(ValueError):
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
        self.listings_dir = '/tmp/wetlands_test_build-listings'
        self.pdfs_dir = 'fixtures/pdfs'
        self.data_dir = '/tmp/wetlands_test_build-data'
        if not os.path.exists(self.listings_dir):
            os.mkdir(self.listings_dir)

