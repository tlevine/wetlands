"""
Test that the right information is extracted from each pdf

Handling null values:
  * No value means that the information has not been processed.
  * None or the empty list indicates that the information is missing from the translated document.
  * The empty string indicates that the value is "".
"""

import os
import unittest
from read import read_public_notice

class TestReadPublicNotice(unittest.TestCase):
    def setUp(self):
        rawtext = open('fixtures/Kilasoethuasoet.pdf.txt').read()
        self.data = read_public_notice(rawtext)
    def test_keys(self):
        observed = set(self.data.keys())
        expected = {
            'WQC',
            'CUP',
            'Mitigation Bank',
            'Acres',
            'Parish',
            'Coords',
            'Basin',
            'HUC',
            '10 acre',
            'Section 10',
            'Section 404',
        }
        self.assertSetEqual(observed, expected)
    def test_types(self):
        observed = {} # Make this
        expected = {
            'WQC': unicode,
            'CUP': unicode,
            'Mitigation Bank': bool,
            'Acres': list,
            'Parish': unicode,
            'Coords': list,
            'Basin': unicode,
#           'HUC',
            '10 acre': bool,
            'Section 10': bool,
            'Section 404': bool,
        }

        set(observed['Acres']).issubset({float})
        set(observed['Coords']).issubset({tuple})
        for c in observed['Coords']:
            # Latitude, longitude
            len(c) == 2
            type(c[0]) == type(c[1]) == float

            # Within a reasonable boundary
            29 < c[0] < 31
            88 < c[1] < 94
            
