import re
import time
import json
import random

import pandas as pd
from selenium import webdriver
import chromedriver_autoinstaller
from urllib.parse import urlencode
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

option = webdriver.ChromeOptions()
option.add_argument('--no-sandbox')
option.add_argument('--disable-dev-sh-usage')
chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]  #크롬드라이버 버전 확인

API_KEY = '163cdcb5666e24f14b838b1530a7ba9b'

music_list = []
album_list = []


caps = DesiredCapabilities.CHROME
caps['goog:loggingPrefs'] = {'performance': 'ALL'}

try:
    driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe',
                                options=option)
except:
    chromedriver_autoinstaller.install(True)
    driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe',
                                options=option)

driver.get('https://www.melon.com/artistplus/finder/index.htm')
driver.find_element(by=By.XPATH, value="//*[@id=\"ntnt03\"]").click()
driver.find_element(by=By.XPATH, value="//*[@id=\"GN0900\"]").click()

# df = pd.DataFrame(columns=['Name','Fans'])
# df.to_csv("artist.csv", mode='a',header=False)
# df = df.append({'Name' : 0, "Fans" : 0}, ignore_index=True)
# print(df)

df = pd.DataFrame(columns=['Name','Fans'])
cnt = 0

driver.find_element(by=By.XPATH, value="//*[@id=\"conts\"]/div[1]/dl/dd/div[2]/button[9]").click()

while True:
    time.sleep(1)
    temp = driver.find_element(by=By.CSS_SELECTOR, value="#pageList")
    cnt_span = temp.find_elements_by_class_name('cnt_span')
    ellipsis = temp.find_elements_by_class_name('ellipsis')

    for j in range(0,len(ellipsis),2):
        if int(cnt_span[j//2].text.replace(",",'')) >= 1000:
            name = ellipsis[j].text
            fan_cnt = int(cnt_span[j//2].text.replace(",",''))
            df = df.append({'Name' : name, "Fans" : fan_cnt}, ignore_index=True)

    if len(cnt_span) < 10:
        break
    cnt += 1

    if cnt % 10 in [1,2,3,4,5,6,7,8,9]:
        driver.find_element(by=By.XPATH, value="//*[@id=\"pageObjNavgation\"]/div/span/a[{}]".format(cnt%10)).click()
    else :
        driver.find_element(by=By.XPATH, value="//*[@id=\"pageObjNavgation\"]/div/a[3]").click()

df.to_csv("artist_{}.csv".format(chr(int(96)+7)), mode='a',header=False)