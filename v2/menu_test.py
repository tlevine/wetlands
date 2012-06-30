import os
import unittest
from menu import menu_parse, menu_save
import json

class TestMenuParse(unittest.TestCase):
    def setUp(self):
        "Load HTML and expected JSON and parse the HTML."
        menu = open(os.path.join('fixtures', 'menu.html'))
        menuData = open(os.path.join('fixtures', 'menu.json'))

        self.html = menu.read()
        self.observedData = menu_parse(self.html)
        self.expectedData = json.loads(menuData.read())

        menu.close()
        menuData.close()

    def test_length(self):
        "The table should have 30 items."
        self.assertEqual(len(self.data), 30)

    def test_types(self):
        "The data should be of appropriate types."
        raise NotImplementedError('')

    def test_data(self):
        "The observed data should equal the expected data."
        self.assertEqual

class TestMenuSave(unittest.TestCase):
    def setUp(self):
        "Load expected JSON."
        menuData = open(os.path.join('fixtures', 'menu.json'))
        self.data = json.loads(menuData.read())
        menuData.close()

        self.connection = pymongo.Connection('desk')
        self.db = self.connection.wetlands_test

    def test_save(self):
        menu_save(self.data, self.db)
        self.db.find
