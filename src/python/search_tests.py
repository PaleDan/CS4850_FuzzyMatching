import unittest
import fuzzy


class SearchTests(unittest.TestCase):

    def test_search(self):
        file = open('db.txt')
        haystack = file.read().splitlines()
        file.close()
        needle = 'Sandra Dodson 376-2877 Aliquet, Rd. Berlin BE'
        results = fuzzy.search(needle, haystack)
        self.assertEqual(needle, results[0]['data'])


if __name__ == '__main__':
    unittest.main()
