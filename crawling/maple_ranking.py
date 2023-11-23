from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from PIL import Image

import requests
import os

async def maple_ranking(path_dir,username):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    

    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    
    driver = webdriver.Chrome(chrome_options=chrome_options)

    driver.set_window_size(2000, 1500)

    url = f"https://maplestory.nexon.com/N23Ranking/World/Total?c={username}&j=13&w=00"
    driver.get(f'https://maplestory.nexon.com/N23Ranking/World/Total?c={username}&j=13&w=0')

    res = requests.get(url)
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
    print(arr)
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
    img_path = sorted(img_path, key=lambda x: int(x.split('\\')[-1].split('.')[0]))

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

