import requests
import csv
import os

from bs4 import BeautifulSoup
from dotenv import load_dotenv

def crawling_event():
    load_dotenv()
    url = os.environ.get("INVEN_URL")

    res = requests.get(url)
    content = res.text
    soup = BeautifulSoup(content, 'html.parser')
    event = soup.select_one('#invenFocus')

    if event:
        rows = event.find_all('p')
        evaent_dat=""
        cnt =0
        for row in rows:
            evaent_dat+=row.text+'\n'
            cnt+=1
            if(cnt%2==0):
                evaent_dat+='\n'
        return evaent_dat


