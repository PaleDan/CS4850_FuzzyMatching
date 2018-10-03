import levenshtein_py
import time
from multiprocessing import Process, Value, Array
from typing import List

def threaded_search(source: str, lookup: List[str]) -> List[dict]:
    search_results = [{'ratio': 0.0}]
    for index, record in enumerate(lookup):
        search_result = levenshtein_py.distance(source, record)
        search_result['data'] = record
        search_result['id'] = index
        search_results.append(result)
        if len(results) > 10:
            search_results.remove(min(search_results, key=lambda x: x['ratio']))
    return search_results


if __name__ == '__main__':
    print('enter the database filename')
    db_file = open(input('>'))
    print('\nenter the search filename')
    search_file = open(input('>'))
    search_list = db_file.read().splitlines()
    db_file.close()

    search_string = search_file.read()
    search_file.close()

    print("beginning search...")
    begin_time = time.process_time()

    results = threaded_search(search_string, search_list)

    end_time = time.process_time()
    print(f"finished search. runtime: {end_time - begin_time} ({end_time} - {begin_time})")

    print('\ntop ten:')
    for result in results:
        print(f"{result['id']}: {result['ratio']}, {result['data']}")
