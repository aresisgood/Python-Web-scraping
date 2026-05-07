import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


def options_set():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-automation"]) # 隱藏「Chrome 正在受到自動測試軟體控制」的提示
    options.add_experimental_option("useAutomationExtension", False) # 停用自動化擴充功能
    ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
    options.add_argument(f"user-agent={ua}") # 讓伺服器知道我們是什麼瀏覽器
    options.add_argument("--start-maximized") # Chrome 瀏覽器在啟動時最大化視窗
    options.add_argument("--incognito") # 無痕模式
    options.add_argument("--disable-popup-blocking") # 停用 Chrome 的彈窗阻擋功能。
    options.add_argument("--disable-blink-features=AutomationControlled") # 關閉自動化特徵
    return options

def open_url(options, comic_num):
    driver = webdriver.Chrome(options=options)
    url = f"https://www.mangaz.com/book/detail/{comic_num}"
    driver.implicitly_wait(10) # 隱性等待
    driver.get(url)
    print("Page Title:", driver.title)
    return driver


def enter_reader(driver):
    button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.open-viewer.book-begin.ga")))
    button.click()

    all_windows = driver.window_handles
    driver.switch_to.window(all_windows[-1])

    Read_Now = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "すぐに読む")))
    Read_Now.click()


def run_scapre(driver, folder_name="manga_screenshots"):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        print(f"已建立資料夾：{folder_name}")
    
    wait_element = WebDriverWait(driver, 10)
    total_image_count = 0
    
    while True:
        image_elements = driver.find_elements(By.CSS_SELECTOR, "div.page_unit.page_image")

        for img_element in image_elements:
            if img_element.is_displayed():
                file_path = f"manga_page_{total_image_count}.png"
                img_element.screenshot(file_path)
                total_image_count += 1

        try:
            next_page = wait_element.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.flip.flip-left")))
            next_page.click()
            print("已點擊下一頁，等待畫面載入...")
            time.sleep(2)
        except TimeoutException:
            print("【系統提示】找不到下一頁按鈕，已達最後一頁，結束爬取迴圈。")
            break

print(f"已完成爬取，共 {total_image_count} 頁，關閉視窗。")
driver.quit()
