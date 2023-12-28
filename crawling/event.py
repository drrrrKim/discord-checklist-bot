import requests
import csv
import os
import logging

from bs4 import BeautifulSoup
from dotenv import load_dotenv

async def crawling_event(path_dir):
    load_dotenv()
    url = os.environ.get("EVENT_URL")
    maple_url = os.environ.get("MAPLESTORY_URL")

    try:
        res = requests.get(url)
        res.raise_for_status()

        content = res.text
        soup = BeautifulSoup(content, 'html.parser')
        event_list = soup.select_one('#container > div > div.contents_wrap > div.event_board > ul')

        if event_list:
            dataset = await extract_event_data(event_list, maple_url)
            headers = ["이벤트명", "기간", "링크"]

            if await write_csv(headers, dataset, path_dir):
                print('csv file create success')
                return True
            else:
                print('csv file create fail')
                return False
        else:
            print('event list empty!')
            return False
        
    except requests.RequestException as e:
        logging.error(f'http request error : {e}')
        return False
    
async def extract_event_data(event_list, maple_url):
    dataset = []
    headers = ["이벤트명", "기간", "링크"]

    rows = event_list.select('li')
    for li in rows:
        data_tag = li.select_one('div.event_list_wrap dl dd.data')
        if data_tag:
            link = data_tag.select_one('p a')['href']
            title = data_tag.select_one('p a').get_text(strip=True)
            date = li.select_one('div.event_list_wrap dl dd.date p').get_text(strip=True)

            columns = [title, date, f'{maple_url}{link}']
            dataset.append(dict(zip(headers, columns)))

    return dataset

async def write_csv(headers, dataset, path_dir):
    try:
        csv_file_path = os.path.join(path_dir, 'data', 'event.csv')
        with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=headers)
            writer.writeheader()

            for data in dataset:
                writer.writerow(data)
        return True
    except Exception as e:
        logging.error(f'csv writer error : {e}')
        return False
