"""
IG資訊抓取，用selenium，含帳號登入
"""
# 爬取ig關鍵字圖片
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import os
import wget
import datetime

"""
WebDriverWait，等待瀏覽器讀取直到出現"*"的標籤
"""

def login_search(PATH, address, account, tpassword, keyword):
    """
    使用selenium登入IG並依據關鍵字搜尋下載圖片，預設滾輪下滾5次讀取
    :param
    PATH : drive path,
    address : web address,
    account and tpassword : for logging in,
    keyword : keyword for searching
    :return:NA, only download photos
    """
    driver = webdriver.Chrome(PATH)
    driver.get(address)

    try:
        username = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )
        password = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "password"))
        )
    except:
        print("無輸入欄位出現")
        driver.quit()
    login = driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]/button')

    username.clear() # 記得先清空input欄位
    password.clear()
    username.send_keys(account)
    password.send_keys(tpassword)
    login.click()

    search = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/input'))
    )
    keyword = keyword # 給輸入的關鍵字參數一個位置
    search.send_keys(keyword)
    time.sleep(2)
    search.send_keys(Keys.RETURN)
    time.sleep(2)
    search.send_keys(Keys.RETURN)  # ig 設定要點兩次 也不能太快

    WebDriverWait(driver, 25).until(
        EC.presence_of_element_located((By.CLASS_NAME, "FFVAD"))
    )  # 等圖片的標籤出現

    for i in range(5):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # 滾到最底
        time.sleep(5)

    imgs = driver.find_elements_by_class_name("FFVAD")
    today = datetime.date.today().strftime('%Y%m%d')
    keyword_path = keyword + today

    path = os.path.join(keyword_path)
    os.mkdir(path)

    count = 0
    for img in imgs:
        save_as = os.path.join(path, keyword + str(count) + '.jpg') # 路徑+檔名
        # print(img.get_attribute("src"))
        wget.download(img.get_attribute("src"), save_as)
        count += 1
        print(f"Downloaded {count} files")

    driver.close()


def main():
    login_search(r"C:\Users\chromedriver.exe", "https://www.instagram.com/",
                 'username', 'password', '# 貓')

main()
