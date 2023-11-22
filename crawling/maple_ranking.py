from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from PIL import Image

import requests
# Setup chrome driver
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
driver.set_window_size(2000, 1500)

url = "https://maplestory.nexon.com/N23Ranking/World/Total?c=%EB%83%89%EA%B5%90&j=13&w=00"
driver.get('https://maplestory.nexon.com/N23Ranking/World/Total?c=%EB%83%89%EA%B5%90&j=13&w=0')

res = requests.get(url)
content = res.text
soup = BeautifulSoup(content, 'html.parser')
target_rows = soup.select('#container > div > div > div:nth-child(4) > div.rank_table_wrap > table > tbody > tr:-soup-contains("냉교")')

id_index=0
# # 원하는 태그의 인덱스를 찾습니다.
for index, row in enumerate(soup.select('#container > div > div > div:nth-child(4) > div.rank_table_wrap > table > tbody > tr')):
    if row in target_rows:
        id_index=index+1
        # print(f"Target row is at index {index}")

arr=[]
arr.append(id_index)
if id_index-1>0:
    arr.append(id_index-1)
if id_index-2>0:
    arr.append(id_index-2)
if id_index+1<11:
    arr.append(id_index+1)
if id_index+2<11:
    arr.append(id_index+2)
arr.sort()
print(arr)
for idx in arr:
    myform = driver.find_element(By.CSS_SELECTOR, f'#container > div > div > div:nth-child(4) > div.rank_table_wrap > table > tbody>tr:nth-child({idx})')
    myform.screenshot(f"../ranking_image/{idx}.png")

# 이미지를 엽니다.
image1 = Image.open("6.png")
image2 = Image.open("7.png")

# 이미지의 크기를 가져옵니다.
width1, height1 = image1.size
width2, height2 = image2.size

# 두 이미지를 수평으로 합칩니다.
combined_image = Image.new('RGB', (max(width1, width2), height1 + height2+height1))
combined_image.paste(image1, (0, 0))
combined_image.paste(image2, (0, height1))
combined_image.paste(image2, (0, height1+height1))

# for file in files:
#     file_path = os.path.join(folder_path, file)
#     if os.path.isfile(file_path) and file.lower().endswith(".png"):
#         folder_name = os.path.basename(os.path.dirname(file_path))
#         print(f"Folder name for {file}: {folder_name}")

# 합쳐진 이미지를 저장합니다.
combined_image.save("combined_image.png")
driver.quit()

