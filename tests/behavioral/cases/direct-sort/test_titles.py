import unittest
from titles import ordered_titles


class TitleTests(unittest.TestCase):
    def test_case_insensitive_order_preserves_spelling(self):
        self.assertEqual(ordered_titles(['Bravo', 'alpha', 'charlie']), ['alpha', 'Bravo', 'charlie'])
