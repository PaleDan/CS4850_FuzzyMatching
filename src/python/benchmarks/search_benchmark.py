import time
import unittest
from search import search_c
from search import search_p


class BenchmarkTests(unittest.TestCase):

    def test_search_c_benchmark(self):
        print('search_c')
        cases = []  # map(lambda x: {'str': x * x, 'data': 1000000}, range(10, 101))

        for case in cases:
            str_size = case['str']
            data_size = case['data']

            needle = 'A' * str_size
            haystack = list(map(lambda x: needle, range(1, data_size)))

            begin = time.process_time()
            search_c(needle, haystack)
            end = time.process_time()
            print(f"{str_size},{end - begin}")
        self.assertEqual(1, 1)

    def test_search_p_benchmark(self):
        print('search_p')
        cases = map(lambda x: {'str': x * x, 'data': 1000}, range(10, 21))

        for case in cases:
            str_size = case['str']
            data_size = case['data']

            needle = 'A' * str_size
            haystack = list(map(lambda x: needle, range(1, data_size)))

            begin = time.process_time()
            search_p(needle, haystack)
            end = time.process_time()
            print(f"{str_size},{end - begin}")
        self.assertEqual(1, 1)

    def test_n_n_benchmark(self):
        cases = [
            # {'str': 10, 'data': 1000},
            # {'str': 10, 'data': 10000},
        ]

        for case in cases:
            str_size = case['str']
            data_size = case['data']
            data = 'A' * str_size
            haystack = list(map(lambda x: data, range(1, data_size)))

            begin = time.time()
            for needle in haystack:
                search_c(needle, haystack)
            end = time.time()
            print(f"{str_size},{data_size} : {end - begin}")
        self.assertEqual(1, 1)

if __name__ == '__main__':
    unittest.main()
