import os
import unittest
import json

class TestPdfQueue(unittest.TestCase):
    pass

class TestPdfSave(unittest.TestCase):
    def setUp(self):
        "Load expected (meta)data."
        self.permitId = ''
        self.expectedMd5 = ''
        self.expectedFilename = ''

    def test_save_notice(self):
        pdf_save(, self.db)
        doc = self.db.findOne(permitId = self.permitId)
        self.assertEqual(doc['md5'], self.expectedMd5)
