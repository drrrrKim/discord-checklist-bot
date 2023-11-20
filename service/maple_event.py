import csv

async def maple_event(path_dir):
    with open(f'{path_dir}/data/event.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        items_weights = []
        next(reader)
        for data in reader:
            items_weights.append(data)
        return items_weights