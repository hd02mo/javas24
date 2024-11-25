import time
import chromedriver_binary # nopa
from selenium import webdriver
#自動更新の奴
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.relative_locator import locate_with

from selenium.common.exceptions import NoSuchElementException
import json


# WebDriver のオプションを設定する
options = webdriver.ChromeOptions()
#options.add_argument('--headless')
#options.add_argument('--no-sandbox')
#Chromeの場所を指定
#options.binary_location = "C:\Program Files\Google\Chrome\Application\chrome.exe"
driver = webdriver.Chrome(options=options)

#コンテストページにアクセス
driver.get('https://atcoder.jp/contests/archive?lang=ja')

#コンテスト一覧のページ数

def get_contests():
    page = 1
    # URLを格納するリスト
    results = []
    while(True):
        driver.get(f'https://atcoder.jp/contests/archive?lang=ja&page={page}&page2=')
        #過去のコンテストページへのURLのテーブル
        try:
            url_table = driver.find_element(By.XPATH,"/html/body/div[1]/div/div[1]/div[3]/div[2]/div/table/tbody")
        except NoSuchElementException:
            break
            
        #urlのテーブル内に含まれる<tr>タグの要素を取得
        rows = url_table.find_elements(By.TAG_NAME, "tr")
        
        # 各<tr>内の<td>を探し、URLを抽出
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")  # 各<tr>内の<td>を取得
            link = cells[1].find_element(By.TAG_NAME, "a")
            contest_title = link.text
            href = link.get_attribute("href")  # URLを取得
            if href:  # hrefが存在すればリストに追加
                #タイトルとurlのセット
                results.append({"コンテスト名":contest_title,"URL":href})
                
        page += 1

    # 抽出したURLを表示
    #print("Extracted URLs:")
    #for url in urls:
    #    print(url)
    
    #次の問題ページへ遷移
    
    return results

def get_tasks(contest_infos):
    task_infos = {"コンテスト名":"コンテストの各問題の情報を格納した辞書のリスト"}
    g_json = open('tasks_info.json','w') #URLリスト開く
    
    for info in contest_infos:
        #新しいコンテストの辞書に、コンテスト名と対応させて問題の情報のリストを空リストとして追加
        task_infos[info["コンテスト名"]] = []

        driver.get(info["URL"])
        task_botton = driver.find_element(By.XPATH,"/html/body/div[3]/div/div[1]/div[1]/ul/li[2]/a")
        href = task_botton.get_attribute("href")  # URLを取得
        driver.get(href)
        url_table = driver.find_element(By.XPATH,"/html/body/div[3]/div/div[1]/div[2]/div[1]/table/tbody")
        rows = url_table.find_elements(By.TAG_NAME, "tr")

        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")  # 各<tr>内の<td>を取得
            task_rank = cells[0].find_element(By.TAG_NAME, "a").text
            link = cells[1].find_element(By.TAG_NAME, "a")
            task_title = link.text
            href2 = link.get_attribute("href")  # URLを取得
            if href2:  # hrefが存在すればリストに追加
                #問題の情報を追加
                task_infos[info["コンテスト名"]].append({"難易度":task_rank,"問題名":task_title,"URL":href2})
                print(f'{href2}',file=g_json)
                
    return task_infos

#問題の分析
def analyze_task(task_infos,contest_infos):
    #繰り返しはコンテストの回数起きる
    for info in contest_infos:
        cont_title = contest_infos["コンテスト名"]
        driver.get(info["URL"]+"/submissions") #提出一覧ページへ遷移

#ユーザのレーティング変化を補足する
def profile_process(url):
    dates = []
    ratings = []
    driver.get(url+"/history")
    check_box = driver.find_element(By.XPATH,"/html/body/div[1]/div/div[1]/div[2]/div[1]/label/input")
    check_box.click() #Ratedのみにする
    driver.find_element(By.XPATH,"/html/body/div[1]/div/div[1]/div[2]/div[2]/div/div[2]/div/table/tbody")
    driver.find_elements(By.TAG_NAME,"tr")
    dates.append()

def user_info_collect():
    page = 1
    user_infos = []
    while(True):
        #コンテストの参加数が5以上のユーザーだけに絞った
        driver.get(f"https://atcoder.jp/ranking?contestType=algo&f.Affiliation=&f.BirthYearLowerBound=0&f.BirthYearUpperBound=9999&f.CompetitionsLowerBound=5&f.CompetitionsUpperBound=9999&f.Country=&f.HighestRatingLowerBound=0&f.HighestRatingUpperBound=9999&f.RatingLowerBound=0&f.RatingUpperBound=9999&f.UserScreenName=&f.WinsLowerBound=0&f.WinsUpperBound=9999&page={page}")
        try:
            users_table = driver.find_element(By.XPATH,"/html/body/div[1]/div/div[1]/div/div[2]/div[2]/table/tbody")
        except NoSuchElementException:
            break
        #urlのテーブル内に含まれる<tr>タグの要素を取得
        rows = users_table.find_elements(By.TAG_NAME, "tr")
        for row in rows:
            users = row.find_elements(By.TAG_NAME, "td")  # 各<tr>内の<td>を取得
            pro_link = users[2].find_elements(By.TAG_NAME, "a")[2]
            href = pro_link.get_attribute("href")  # URLを取得
            user_name = pro_link.find_element(By.TAG_NAME, "span").text

            profile_process(href) = 

            if href:  # hrefが存在すればリストに追加
                user_infos.append({"ユーザー名":user_name,"URL":href})
        page += 1


            

get_tasks(get_contests())

driver.quit()

