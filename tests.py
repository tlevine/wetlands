#!/usr/bin/env python2
# -*- encoding: utf-8 -*-

import unittest
from demjson import encode
from dumptruck import DumpTruck
import os

import excavate

class DummyBucket:
    bucket = 'dummy'
    motherbucket = 'rocket scientist'
    def __init__(self, *args, **kwargs):
        self.init_params = [args, kwargs]

    def tojson(self):
        return [[],{}]

class BaseBag(unittest.TestCase):
    def setUp(self):
        excavate.dt.drop('_bag', if_exists = True)
        self.bag = excavate.Bag()
        self.bucket = DummyBucket()

    def test_add(self):
        self.bag.add(self.bucket)
        self.bag.add(self.bucket)
        self.bag.add(self.bucket)
        self.bag.add(self.bucket)
        observed = excavate.dt.dump('_bag')
        expected = [{
            u'Bucket': u'dummy',
            u'MotherBucket': u'rocket scientist',
            u'__init__': [[], {}],
        }] * 4
        self.assertEqual(observed, expected)

if __name__ == '__main__':
    unittest.main()
