import time
import unittest
from search import search


class BenchmarkTests(unittest.TestCase):

    def test_benchmark(self):
        cases = [
            {'str': 10, 'data': 1000000},
            {'str': 10, 'data': 10000000},
            {'str': 20, 'data': 1000000},
            {'str': 20, 'data': 10000000},
            {'str': 30, 'data': 1000000},
            {'str': 30, 'data': 10000000},
            {'str': 40, 'data': 1000000},
            {'str': 40, 'data': 10000000},
            {'str': 50, 'data': 1000000},
            {'str': 50, 'data': 10000000},
            {'str': 60, 'data': 1000000},
            {'str': 60, 'data': 10000000},
        ]

        for case in cases:
            str_size = case['str']
            data_size = case['data']

            needle = 'A' * str_size
            haystack = list(map(lambda x: needle, range(1, data_size)))

            begin = time.time()
            search(needle, haystack)
            end = time.time()
            print(f"{str_size},{data_size} : {end - begin}")
        self.assertEqual(1, 1)

    def test_n_n_benchmark(self):
        cases = [
            {'str': 10, 'data': 1000},
            {'str': 10, 'data': 10000},
        ]

        for case in cases:
            str_size = case['str']
            data_size = case['data']
            data = 'A' * str_size
            haystack = list(map(lambda x: data, range(1, data_size)))

            begin = time.time()
            for needle in haystack:
                search(needle, haystack)
            end = time.time()
            print(f"{str_size},{data_size} : {end - begin}")


if __name__ == '__main__':
    unittest.main()
