import time
import chromedriver_binary # nopa
import requests
from selenium import webdriver
#自動更新の奴
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.relative_locator import locate_with
from bs4 import BeautifulSoup

def get_task_auto():
    # WebDriver のオプションを設定する
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    #Chromeの場所を指定
    options.binary_location = "C:\Program Files\Google\Chrome\Application\chrome.exe"
    driver = webdriver.Chrome(options = options)

    #コンテストページにアクセス
    driver.get('https://atcoder.jp/contests/archive?lang=ja')

    #過去のコンテストページへのURLのテーブル
    url_table = driver.find_element(By.XPATH,"/html/body/div[1]/div/div[1]/div[3]/div[2]/div/table/tbody")
    #urlのテーブル内に含まれる<tr>タグの要素を取得
    rows = url_table.find_elements(By.TAG_NAME, "tr")
    # URLを格納するリスト
    urls = []
    
    # 各<tr>内の<td>を探し、URLを抽出
    for row in rows:
        cells = row.find_elements(By.TAG_NAME, "td")  # 各<tr>内の<td>を取得
        link = cells[1].find_element(By.TAG_NAME, "a")
        href = link.get_attribute("href")  # URLを取得
        if href:  # hrefが存在すればリストに追加
            urls.append(href)

    # 抽出したURLを表示
    print("Extracted URLs:")
    for url in urls:
        print(url)

    # ブラウザを閉じる
    driver.quit()


get_task_auto()

