import requests
import csv
import os

from bs4 import BeautifulSoup
from dotenv import load_dotenv

async def crawling_event(path_dir):
    load_dotenv()
    url = os.environ.get("EVENT_URL")
    maple_url = os.environ.get("MAPLESTORY_URL")

    res = requests.get(url)
    content = res.text
    soup = BeautifulSoup(content, 'html.parser')
    ul = soup.select_one('#container > div > div.contents_wrap > div.event_board > ul')
    dataset=[]
    headers=["이벤트명","기간","링크"]

    if ul:
        rows = ul.select('li')
        for li in rows:
            data_tag = li.select_one('div.event_list_wrap dl dd.data')
            if data_tag:
                link = data_tag.select_one('p a')['href']
                title = data_tag.select_one('p a').get_text(strip=True)
                date = li.select_one('div.event_list_wrap dl dd.date p').get_text(strip=True)

                columns = [title, date,f'{maple_url}{link}']
                dataset.append(dict(zip(headers, columns)))

        if await csv_event(headers,dataset,path_dir):
            print('create csv sucess')
            return True
        else:
            print('create csv fail')
            return False
    else:
        print('ul no data')

async def csv_event(headers, dataset,path_dir):
    try:
        csv_file_path = f'{path_dir}/data/event.csv'
        with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=headers)
            writer.writeheader()
            
            for data in dataset:
                writer.writerow(data)
        return True
    except Exception as e:
        print(e)
        return False