#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import time
# 設定ファイル
import configparser

# --------------------------------------------------
# configparserの宣言とiniファイルの読み込み
# --------------------------------------------------
config = configparser.ConfigParser()
config.read('config.ini', encoding='utf-8')

URL = config['SCRAGING']['URL']
REGISTER_ID = config['SCRAGING']['REGISTER_ID']

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys

options = Options()
options.download_manager = ChromeDriverManager().install()
# options.add_argument('--headless') # ヘッドレス起動

driver = webdriver.Chrome(options=options)
driver.get(URL)

time.sleep(1)

msg = driver.find_element(By.ID, "ExportCheckMsg")
input = driver.find_element(By.ID, "ExportNotify")
input.send_keys(REGISTER_ID, Keys.ENTER)
# dropdown.click()
print(msg.text)


select_elm = driver.find_element(By.ID, "ExportMethod")
select = Select(select_elm)
#セレクトタグのオプションをインデックス番号から選択する
select.select_by_index(len(select.options)-1)

time.sleep(3)

# htmlを取得・表示
html = driver.page_source
# print(html)

# ブラウザーを終了
driver.quit()

#ExportCheckMsg
# ExportNotify