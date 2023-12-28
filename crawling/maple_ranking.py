from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from PIL import Image
from concurrent.futures import ThreadPoolExecutor

import requests
import os
import logging

async def maple_ranking(path_dir,username, bera, job):
    with ThreadPoolExecutor() as executor:
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.implicitly_wait(10)

        url = f"https://maplestory.nexon.com/N23Ranking/World/Total?c={username}{job}&w={bera}"
        driver.get(f'https://maplestory.nexon.com/N23Ranking/World/Total?c={username}{job}&w={bera}')
    
        try:
            res = requests.get(url)
            res.raise_for_status()

            content = res.text

            soup = BeautifulSoup(content, 'html.parser')
            target_user_name = soup.select(f'#container > div > div > div:nth-child(4) > div.rank_table_wrap > table > tbody > tr:-soup-contains({username})')

            user_index=0

            for index, row in enumerate(soup.select('#container > div > div > div:nth-child(4) > div.rank_table_wrap > table > tbody > tr')):
                if row in target_user_name:
                    user_index=index+1

            arr=[]
            arr.append(user_index)
            if user_index-1>0:
                arr.append(user_index-1)
            if user_index-2>0:
                arr.append(user_index-2)
            if user_index+1<11:
                arr.append(user_index+1)
            if user_index+2<11:
                arr.append(user_index+2)
            arr.sort()

            for idx in arr:
                myform = driver.find_element(By.CSS_SELECTOR, f'#container > div > div > div:nth-child(4) > div.rank_table_wrap > table > tbody>tr:nth-child({idx})')
                myform.screenshot(f"{path_dir}/ranking_image/{idx}.png")

            folder_path=f'{path_dir}/ranking_image'
            files = os.listdir(folder_path)

            img_path=[]
            for file in files:
                file_path = os.path.join(folder_path, file)
                if os.path.isfile(file_path) and file.lower().endswith(".png"):
                    img_path.append(file_path)
            # img_path = sorted(img_path, key=lambda x: int(x.split('\\')[-1].split('.')[0]))
            img_path = sorted(img_path, key=lambda x: int(x.split('/')[-1].split('.')[0]))


            result_image=Image.open(img_path[0])
            for img in img_path[1:]:
                image1 = result_image
                image2 = Image.open(img)

                width1, height1 = image1.size
                width2, height2 = image2.size

                combined_image = Image.new('RGB', (max(width1, width2), height1 + height2))
                combined_image.paste(image1, (0, 0))
                combined_image.paste(image2, (0, height1))
                result_image=combined_image

            result_image.save(f"{path_dir}/test.png")
            driver.quit()
            try:
                files = os.listdir(folder_path)

                for file in files:
                    file_path = os.path.join(folder_path, file)
                    if os.path.isfile(file_path):
                        os.remove(file_path)
            except Exception as e:
                print(f"error: {e}")
        except requests.RequestException as e:
            logging.error(f'http request error : {e}')
            return False
