import levenshtein
import time
from typing import List


def search(source: str, lookup: List[str]) -> List[dict]:
    results = [{'ratio': 0.0}]
    for index, record in enumerate(lookup):
        result = levenshtein.distance(source, record)
        result['data'] = record
        result['id'] = index
        results.append(result)
        if len(results) > 10:
            results.remove(min(results, key=lambda x: x['ratio']))
    return results


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
