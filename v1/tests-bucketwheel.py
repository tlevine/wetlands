#!/usr/bin/env python2
# -*- encoding: utf-8 -*-

import unittest
from demjson import encode
from dumptruck import DumpTruck
import os

import bucketwheel
# Hack for faster runnig
def refreshdb():
    os.system('rm /tmp/wetlands.sqlite')
    bucketwheel.dt = DumpTruck(
        dbname = '/tmp/wetlands.sqlite',
        auto_commit = False
    )
refreshdb()

class DummyBucket:
    bucket = u'DummyBucket'
    motherbucket = None
    def __init__(self, **kwargs):
        self.kwargs = kwargs

class Grandpa(bucketwheel.BucketMold):
    bucket = 'Grandpa'

class Pa(bucketwheel.BucketMold):
    bucket = 'Pa'
    motherbucket = 'Grandpa'

class Bro(bucketwheel.BucketMold):
    bucket = 'Bro'
    motherbucket = 'Pa'

class FamilyBag(unittest.TestCase):
    def setUp(self):
        refreshdb()
        self.bag = bucketwheel.Bag(buckets = [Grandpa, Pa, Bro])

    def test_tables_count(self):
        self.assertSetEqual(bucketwheel.dt.tables(), {'Grandpa', 'Pa', 'Bro', '_bag'})

class BaseBag(unittest.TestCase):
    def setUp(self):
        bucketwheel.dt.drop('_bag', if_exists = True)
        self.bag = bucketwheel.Bag(buckets = [DummyBucket])
        self.bucket = DummyBucket()

class TestBagAdd(BaseBag):
    def test_add(self):
        self.bag.add(self.bucket)
        self.bag.add(self.bucket)
        self.bag.add(self.bucket)
        self.bag.add(self.bucket)
        observed = bucketwheel.dt.execute('select Bucket, MotherBucket, kwargs from _bag')
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
        self.assertListEqual([], bucketwheel.dt.dump('_bag'))

if __name__ == '__main__':
    unittest.main()
