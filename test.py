from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# 仮想ディスプレイを開始
display = Display(visible=0, size=(1920, 1080))
display.start()

# WebDriverのセットアップ
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

driver.get("https://www.google.com")
print(driver.title)

# 終了処理
driver.quit()
display.stop()
