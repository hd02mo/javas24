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
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re


# WebDriver のオプションを設定する
def initialize_driver():
    options = webdriver.ChromeOptions()
    #options.add_argument("--headless")  
    options.add_argument("--no-sandbox")
    options.add_argument(r"--user-data-dir=C:\\Users\\utaku\\AppData\\Local\\Google\\Chrome\\User Data")  # プロファイルのディレクトリ
    options.add_argument(r"--profile-directory=Default")  # プロファイル名（Default, Profile 1, など）
    return webdriver.Chrome(options=options)

#コンテスト一覧のページ数

def get_contests(driver):
    page = 1
    contests = open('contest_infos.json','w') #urlの一覧のtxtファイル
    # URLを格納するリスト
    results = []
    while(True):
        driver.get(f'https://atcoder.jp/contests/archive?category=&keyword=Atcoder+Beginner+Contest&page={page}&ratedType=0')
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
                results.append({"contest_name":re.search(r"AtCoder Beginner Contest \d+", contest_title).group(),"URL":href})
                
        page += 1
    
    json.dump(results,contests,indent = 4,ensure_ascii=False)
    contests.close()

def get_tasks(contest_infos_title,driver,load_i = 0,load_task_infos = {}):
    contest_infos = json.load(open(contest_infos_title,'r')) #コンテストのjsonファイル開き、中身を読み込む
    
    task_infos = load_task_infos #  "コンテスト名" : "コンテストの各問題の情報を格納した辞書のリスト"
    g_json = open('tasks_info.json','w',encoding="utf-8") #URLリスト開く aオプションで追加する形
    
    for i in range(load_i,len(contest_infos)):
        info = contest_infos[i]
        
        #新しいコンテストの辞書に、コンテスト名と対応させて問題の情報のリストを空リストとして追加
        task_infos[info["contest_name"]] = []
        
        try:
            driver.get(info["URL"]) 
            WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located)  #読み込みに最大十秒待機
            task_botton = driver.find_element(By.XPATH,"/html/body/div[3]/div/div[1]/div[1]/ul/li[2]/a")
            href = task_botton.get_attribute("href")  # URLを取得
            driver.get(href)
            WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located) #読み込みに最大十秒待機
            url_table = driver.find_element(By.XPATH,"/html/body/div[3]/div/div[1]/div[2]/div[1]/table/tbody")
            rows = url_table.find_elements(By.TAG_NAME, "tr")
            
        except:
            driver.quit()
            time.sleep(180)            
            driver = initialize_driver()
            g_json.close()
            return get_tasks(contest_infos_title,driver,i,task_infos) #同じ条件で自身を起動

        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")  # 各<tr>内の<td>を取得
            task_rank = cells[0].find_element(By.TAG_NAME, "a").text
            link = cells[1].find_element(By.TAG_NAME, "a")
            task_title = link.text
            href2 = link.get_attribute("href")  # URLを取得
            if href2:  # hrefが存在すればリストに追加
                #問題の情報を追加
                task_infos[info["contest_name"]].append({"level":task_rank,"title":task_title,"url":href2})
    json.dump(task_infos, g_json, indent = 4)
    g_json.close()
    return task_infos

#問題の分析
def analyze_task(driver):
    name_and_urls = json.load(open("name_and_urls.json",'r')) #url、名前の順
    #繰り返しはコンテストの回数起きる
    #ABC19までは Task=abc019_1 以降はTask=abc019_a
    load_i_di_pi = json.load(open("_to_save_analyze_task.json",'r')) #セーブ用のjsonファイル開き、中身を読み込む
    load_i = load_i_di_pi[0]
    load_di = load_i_di_pi[1]
    
    load_date_ls = load_i_di_pi[3]
    load_name_ls = load_i_di_pi[4]
    load_lang_ls = load_i_di_pi[5]
    load_time_ls = load_i_di_pi[6]
    
    contest_infos = json.load(open('contest_infos.json','r')) #get_contestsで作成したリスト
    task_infos = json.load(open('analyze_tasks.json','r')) #get_tasksで作成した問題の情報の辞書
    
    
    difficulties1 = ["a","b","c","d","e","f","g","h","i","j"]
    difficulties2 = [1,2,3,4,5,6,7,8,9,10]
    for i in range(load_i , len(contest_infos)):
        info = contest_infos[i]
        contest_title = contest_infos[i]["contest_name"]
        cont_num = re.search(r"\d+", contest_title).group() #第何回コンテストか
        
        if(int(cont_num) > 19):
            difficulties = difficulties1 #19回以降なら、難易度abc表記
        else:
            difficulties = difficulties2 #19回までなら、難易度1,2,3...表記
            
        for di in range(load_di , len(difficulties)):
            d = difficulties[di]
            #提出一覧ページへ遷移ただしACかつユーザを分けている
            user_set = set()
            date_ls = load_date_ls
            name_ls = load_name_ls
            lang_ls = load_lang_ls
            time_ls = load_time_ls
            
            try:
                pi = load_i_di_pi[2] #ページ番号の初期値、中断したなら続きから
                driver.get(info["URL"] + f"/submissions?f.Task=abc{cont_num}_{d}&f.LanguageName=&f.Status=AC&f.User=&page={pi}")
                print(info["URL"] + f"/submissions?f.Task=abc{cont_num}_{d}&f.LanguageName=&f.Status=AC&f.User=&page={pi}")
                #time.sleep(15)
                while(True):
                    tbody = driver.find_element(By.XPATH,"/html/body/div[3]/div/div[1]/div[3]/div/div[2]/table/tbody")
                    trs = tbody.find_elements(By.TAG_NAME,"tr")
                    for tr in trs: #一つのtrが一人のユーザーに対応する
                        
                        name = tr.find_element(By.XPATH,"./td[3]/a[1]").text #名前
                
                        #すでに調べたユーザーでなく、かつコンテスト五回以上参加のアクティブなuserのデータであるか、という判定
                        if(not (name in user_set) and (name == n[1] for n in name_and_urls)):
                            user_set.add(name)
                        else:
                            continue
                        
                        date = tr.find_element(By.XPATH,"./td[1]/time").text #日時
                        lang = tr.find_element(By.XPATH,"./td[4]/a").text #使用言語
                        run_time = tr.find_element(By.XPATH,"./td[8]").text #実行時間
                        date_ls.append(date)
                        name_ls.append(name)
                        lang_ls.append(lang)
                        time_ls.append(run_time)
                            
                    pi += 1
                    next_button = driver.find_element(By.XPATH,"/html/body/div[3]/div/div[1]/div[3]/nav[1]/ul/li[2]")
                    class_name = next_button.get_attribute("class")
                    if(class_name == "disabled"): #ボタンが押せない場合
                        load_i_di_pi[2] = 1 #リセット
                        break
                    else:
                        #次のページに遷移するボタンを押す
                        next_button.click()
                        
                task_dic = task_infos[info["contest_name"]][di] #task_infos内の、今調べてるコンテスト内の、di番目の問題の情報を入れた辞書
                task_dic["date list"] = date_ls
                task_dic["name list"] = name_ls
                task_dic["lang list"] = lang_ls
                task_dic["run time list"] = time_ls
                
                
            except:
                driver.quit()
                time.sleep(180)
                to_save = open("_to_save_analyze_task.json",'w') #書き込む用に開く。
                json.dump([i,di,pi,date_ls,name_ls,lang_ls,time_ls],to_save) #エラーが起きた時の、i・diなどを保存しとく
                to_save.close()
                g_json = open('analyze_tasks.json','w',encoding="utf-8")
                json.dump(task_infos, g_json, indent = 4)
                return False #まだ残ってますよ、の意味 これ書き込まないと進捗失われないか？
            
        load_di = 0 #リセット
        date_ls = []
        name_ls = []
        lang_ls = []
        time_ls = []
        
    g_json = open('analyze_tasks.json','w',encoding="utf-8")
    json.dump(task_infos, g_json, indent = 4)
    g_json.close()
    return True #もう調べ終わりましたよ、の意味
                    
def name_url_collect(driver,load_page = 1 , load_profile_name_ls = []):
    g_json = open('name_and_urls.json','w',encoding="utf-8") #URLリスト開く aオプションで追加する形
    page = load_page
    profile_name_ls = load_profile_name_ls
    while(True):
        try:
        #コンテストの参加数が5以上のユーザーだけに絞った
            driver.get(f"https://atcoder.jp/ranking?contestType=algo&f.Affiliation=&f.BirthYearLowerBound=0&f.BirthYearUpperBound=9999&f.CompetitionsLowerBound=5&f.CompetitionsUpperBound=9999&f.Country=&f.HighestRatingLowerBound=0&f.HighestRatingUpperBound=9999&f.RatingLowerBound=0&f.RatingUpperBound=9999&f.UserScreenName=&f.WinsLowerBound=0&f.WinsUpperBound=9999&page={page}")
        except:
            driver.quit()
            time.sleep(180)            
            driver = initialize_driver()
            g_json.close()
            return get_tasks(driver,page,profile_name_ls) #同じ条件で自身を起動
        
        try:    
            users_tbody = driver.find_element(By.XPATH,"/html/body/div[1]/div/div[1]/div/div[2]/div[2]/table/tbody")
            
        except NoSuchElementException:
            json.dump(profile_name_ls, g_json, indent = 4)
            g_json.close()
            return
            
        #urlのテーブル内に含まれる<tr>タグの要素を取得
        rows = users_tbody.find_elements(By.TAG_NAME, "tr")
        for row in rows:
            users = row.find_elements(By.TAG_NAME, "td")  # 各<tr>内の<td>を取得
            pro_link = users[1].find_elements(By.TAG_NAME, "a")[1]
            href = pro_link.get_attribute("href")  # URLを取得
            user_name = pro_link.find_element(By.TAG_NAME, "span").text #ユーザー名
            if href: #ぷろふぃーるのurlが存在するなら追加
                profile_name_ls.append((href,user_name))
        page += 1
            
            
#ユーザのレーティング変化を補足する(user_info_collectの一部)
def profile_process(url,driver):
    dates = []
    ratings = []
    driver.get(url+"/history")
    check_box = driver.find_element(By.XPATH,"/html/body/div[1]/div/div[1]/div[2]/div[1]/label/input")
    check_box.click() #Ratedのみにする
    table = driver.find_element(By.XPATH,"/html/body/div[1]/div/div[1]/div[2]/div[2]/div/div[2]/div/table/tbody")
    trs = table.find_elements(By.TAG_NAME,"tr")
    for tr in trs:
        date = tr.find_element(By.XPATH,"/td[1]/time").text
        dates.append(date)
        rating = tr.find_element(By.XPATH,"/td[4]/span").text
        ratings.append(rating)
    return dates , ratings

    
def user_info_collenct(driver,load_i = 0, load_user_infos = {}):
    name_and_urls = json.load(open("name_and_urls.json",'r'))
    user_infos = load_user_infos
    g_json = open('user_infos.json','w',encoding="utf-8")
    
    for i in range(load_i,len(name_and_urls)):
        href = name_and_urls[i][0]
        user_name = name_and_urls[i][1]
        try:
            dates , ratings = profile_process(href,driver) #プロフィールに遷移してユーザーデータをとる
            user_infos[user_name] = {"date_list" :dates,"rating_list" :ratings}
            
        except:
            driver.quit()
            time.sleep(180)            
            driver = initialize_driver()
            g_json.close()
            user_info_collenct(driver,i,user_infos)
            
    
    json.dump(user_infos,g_json)   
    
    
        
        

     
Driver = initialize_driver()
#コンテストページにアクセス
Driver.get('https://atcoder.jp/contests/archive?lang=ja')

#name_url_collect(Driver)

#get_contests(Driver)
#get_tasks("contest_infos.json",Driver)

while(True):
    if(analyze_task(Driver)):
        break
    else:
        Driver = initialize_driver()
        
Driver.quit()

