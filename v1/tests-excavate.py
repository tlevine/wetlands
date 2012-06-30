#!/usr/bin/env python2
# -*- encoding: utf-8 -*-

import unittest
import tempfile
import os
from excavate import pdftoxml, pdftotext, pdfto

class TestPdfTo(unittest.TestCase):
    def setUp(self):
        self.pdf = open('pdf/MVN-2002-3090-EFF/FINAL-JPN.pdf').read()

    def test_pdftoxml(self):
        'Test that the version based on pdfto works like the above hard-coded one'
        self.assertEquals(pdftoxml(self.pdf), self._pdftoxml(self.pdf))

    @staticmethod
    def _pdftoxml(pdfdata):
        """
        Fixture for testing excavate.pdfto
        converts pdf file to xml file, from scraperlibs
        """
        pdffout = tempfile.NamedTemporaryFile(suffix='.pdf')
        pdffout.write(pdfdata)
        pdffout.flush()

        xmlin = tempfile.NamedTemporaryFile(mode='r', suffix='.xml')
        tmpxml = xmlin.name # "temph.xml"
        cmd = '/usr/bin/pdftohtml -xml -nodrm -zoom 1.5 -enc UTF-8 -noframes "%s" "%s"' % (pdffout.name, os.path.splitext(tmpxml)[0])
        cmd = cmd + " >/dev/null 2>&1" # can't turn off output, so throw away even stderr yeuch
        print(cmd)
        os.system(cmd)

        pdffout.close()
        #xmlfin = open(tmpxml)
        xmldata = xmlin.read()
        xmlin.close()
        return xmldata

if __name__ == '__main__':
    unittest.main()
