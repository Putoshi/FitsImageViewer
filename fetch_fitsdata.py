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

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

options = Options()
options.download_manager = ChromeDriverManager().install()
# options.add_argument('--headless') # ヘッドレス起動

driver = webdriver.Chrome(options=options)
driver.get(URL)

time.sleep(5)

# htmlを取得・表示
html = driver.page_source
print(html)

# ブラウザーを終了
driver.quit()

#ExportCheckMsg
# ExportNotify