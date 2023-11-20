import csv

async def symbol_cost(path_dir, symbol, start_num, end_num):
    with open(f'{path_dir}/data/symbol_cost.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader) 

        result_symbol=0
        result_price=0

        for row in reader:
            level=int(row[0])
            if start_num <= level < end_num:
                result_symbol+=int(row[1])
                result_price+=int(row[symbol])

        return result_price, result_symbol
