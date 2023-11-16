import csv
import random

async def choice_wonki_berry(path_dir, number):
    with open(f'{path_dir}/data/wonkiberry.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader) 

        items_weights = []

        for row in reader:
            probability = float(row[0][:-1]) / 100.0 
            item = row[1]
            items_weights.append((item, probability))

    result_items = [item for item, _ in random.choices(items_weights, weights=[weight for _, weight in items_weights], k=number)]
    
    return result_items
