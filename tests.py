#!/usr/bin/env python2
# -*- encoding: utf-8 -*-

import unittest
from demjson import encode
from dumptruck import DumpTruck
import os

import excavate
# Hack for faster runnig
excavate.dt = DumpTruck(
    dbname = '/tmp/wetlands.sqlite',
    auto_commit = False
)

class DummyBucket:
    bucket = u'DummyBucket'
    motherbucket = None
    def __init__(self, **kwargs):
        self.kwargs = kwargs

class BaseBag(unittest.TestCase):
    def setUp(self):
        excavate.dt.drop('_bag', if_exists = True)
        self.bag = excavate.Bag(buckets = [DummyBucket])
        self.bucket = DummyBucket()

class TestBagAdd(BaseBag):
    def test_add(self):
        self.bag.add(self.bucket)
        self.bag.add(self.bucket)
        self.bag.add(self.bucket)
        self.bag.add(self.bucket)
        observed = excavate.dt.execute('select Bucket, MotherBucket, kwargs from _bag')
        expected = [{
            u'Bucket': u'DummyBucket',
            u'MotherBucket': None, #u'RocketScientistBucket',
            u'kwargs': {},
        }] * 4
        self.assertListEqual(observed, expected)

class TestBagAddPop(BaseBag):
    def test_add_pop(self):
        original = self.bucket
        self.bag.add(self.bucket)
        popped = self.bag.pop()
        self.assertDictEqual(original.kwargs, popped.kwargs)
        self.assertListEqual([], excavate.dt.dump('_bag'))

if __name__ == '__main__':
    unittest.main()
