import requests
import csv
import os
import logging

from bs4 import BeautifulSoup
from dotenv import load_dotenv

async def crawling_royal(path_dir):
    load_dotenv()
    url = os.environ.get("ROYAL_URL")

    try:
        res = requests.get(url)
        res.raise_for_status()

        content = res.text
        soup = BeautifulSoup(content, 'html.parser')
        table = soup.select_one('#container > div > div.contents_wrap > table')

        dataset = []

        if table:
            rows = table.find_all('tr')
        
            header_row = rows[0]
            headers = [header.get_text(strip=True) for header in header_row.find_all('th')[1:]]
            headers = list(reversed(headers))

            for row in rows[1:]:
                columns = [col.get_text(strip=True) for col in reversed(row.find_all('td'))]
                dataset.append(dict(zip(headers, columns)))
        
            if await write_csv(headers, dataset, path_dir):
                print('csv file create success')
                return True
            else:
                print('csv file create fail')
                return False
        else:
            print('royal list empty!')
            return False
        
    except requests.RequestException as e:
        logging.error(f'http request error : {e}')
        return False
    
async def write_csv(headers, dataset, path_dir):
    try:
        csv_file_path = os.path.join(path_dir, 'data', 'royal.csv')
        with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=headers)
            writer.writeheader()

            for data in dataset:
                writer.writerow(data)
        return True
    except Exception as e:
        logging.error(f'csv writer error : {e}')
        return False