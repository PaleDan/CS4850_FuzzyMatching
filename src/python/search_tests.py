import unittest
from search import search


class SearchTests(unittest.TestCase):

	def test_search(self):
		file = open('db100k.txt')
		haystack = file.read().splitlines()
		file.close()
		needle = 'Sandra Dodson 376-2877 Aliquet, Rd. Berlin BE'
		print('haystack:' + str(len(haystack)))
		results = search(needle, haystack)
		self.assertEqual(needle, results[0]['data'])


if __name__ == '__main__':
	unittest.main()
