import Levenshtein
import time
from typing import List


def search(source: str, lookup: List[str]) -> List[dict]:
    search_results = [{'ratio': 0.0}]
    for index, record in enumerate(lookup):
        ratio = Levenshtein.ratio(source, record)
        search_result = {'ratio': ratio, 'data': record, 'id': index}
        search_results.append(search_result)
        if len(search_results) > 10:
            search_results.remove(min(search_results, key=lambda x: x['ratio']))
    search_results.sort(key=lambda x: x['ratio'], reverse=True)
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

    results = search(search_string, search_list)

    end_time = time.process_time()
    print(f"finished search. runtime: {end_time - begin_time} ({end_time} - {begin_time})")

    print('\ntop ten:')
    for result in results:
        print(f"{result['id']}: {result['ratio']}, {result['data']}")
