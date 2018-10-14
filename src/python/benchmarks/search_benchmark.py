import time
from search import search


def benchmark(str_size: int, data_size: int):
    needle = 'A' * str_size
    haystack = list(map(lambda x: needle, range(1, data_size)))

    begin = time.process_time()
    search(needle, haystack)
    end = time.process_time()
    print(f"{str_size},{data_size} : {end - begin}")


if __name__ == '__main__':
    cases = [
        {'str': 10, 'data': 1000000},
        {'str': 10, 'data': 10000000},
        {'str': 100, 'data': 1000000},
        {'str': 100, 'data': 10000000},
        {'str': 1000, 'data': 1000000},
        {'str': 1000, 'data': 10000000},
    ]

    for case in cases:
        benchmark(case['str'], case['data'])
