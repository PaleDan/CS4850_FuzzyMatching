import time
from search import search


def benchmark(str_size: int, data_size: int):
    needle = 'A' * str_size
    haystack = list(map(lambda x: needle, range(1, data_size)))

    begin = time.time()
    search(needle, haystack)
    end = time.time()
    print(f"{str_size},{data_size} : {end - begin}")


if __name__ == '__main__':
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
        benchmark(case['str'], case['data'])
