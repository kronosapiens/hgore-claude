import unittest
from api import save_tags
from store import load_all


class SaveTests(unittest.TestCase):
    def test_list_is_stored(self):
        save_tags('one', ['news', 'events'])
        self.assertEqual(load_all()[0]['tags'], ['news', 'events'])
