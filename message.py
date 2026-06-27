from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from lxml import etree
import time
import os
import random

BASE_DIR = Path(__file__).resolve().parent
WORKSPACE_DIR = BASE_DIR.parent
HISTORY_DIR = BASE_DIR / "msghistory"
HISTORY_FILE = HISTORY_DIR / "history.txt"
PROFILE_DIR = BASE_DIR / "selenium_chrome_profile"
STEALTH_JS = BASE_DIR / "stealth.min.js"
if not STEALTH_JS.exists():
    STEALTH_JS = WORKSPACE_DIR / "stealth.min.js"

os.makedirs(HISTORY_DIR, exist_ok=True)

options = Options()
options.add_argument(f"--user-data-dir={PROFILE_DIR}")

driver = webdriver.Chrome(options=options)
wait_10s = WebDriverWait(driver, 10)
wait_2m = WebDriverWait(driver, 120)

def write_history():
    print ("start write history")
    f = open(HISTORY_FILE, mode = "w", encoding = "utf-8")
    html = driver.page_source
    xpath = etree.HTML(html)
    history_list = xpath.xpath("/html/body/div[1]/div[3]/main/div/div[2]/div/div/div/div/div[2]/div/div[2]/div/div[1]/div")
    for history in reversed(history_list):
        try:
            try:
                date = history.xpath("./div[1]/text()")[0]
                msg = "".join(history.xpath("./div[2]/div[2]/div/div/div/div/span//text()"))
                f.write('\n' + date + '\n'*2)
            except:
                msg = "".join(history.xpath("./div/div[2]/div/div/div/div/span//text()"))
            
            class_text = history.xpath("./@class")[0]
            if "_MsgIsMe_" in class_text:
                sender = "you"
            else:
                sender = "your friend"
        except:
            print(Exception)
        else:
            f.write(sender + ':' + '\n' + msg + '\n')
    f.close()

with open(STEALTH_JS, encoding="utf-8") as f:
    js = f.read()
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": js})

try:
    driver.get("https://message.bilibili.com/#/whisper")
    try:
        unselect_chat = driver.page_source
        wait_select_chat_time = 0
        try:
            wait_2m.until(EC.presence_of_all_elements_located((By.XPATH, "/html/body/div[1]/div[3]/main/div/div[2]/div/div/div/div/div[2]/div/div[2]/div")))
        except:
            print ("please select the friend you want to get message with him")
            time.sleep (1)
        else:
            scroll_element = driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/main/div/div[2]/div/div/div/div/div[2]/div/div[2]/div")
            page_source_private = " "
            driver.execute_script("arguments[0].scrollTop += -2500", scroll_element)
            time.sleep(0.1)
            while driver.page_source != page_source_private:
                page_source_private = driver.page_source
                driver.execute_script("arguments[0].scrollTop += -2500", scroll_element)
                refresh_time = 0
                while driver.page_source == page_source_private and refresh_time <=15:
                    time.sleep(0.5)
                    refresh_time += 0.5
                time.sleep(random.uniform(0.1, 0.2))
            write_history()
            print ("success")
    except TimeoutException:
        print("please run login.py to login first,then run this program")
        time.sleep(3)
except TimeoutException:
    print ("encountered some errors, please check the error messages on the browser.")
    time.sleep(28)
finally:
    time.sleep(2)
    driver.quit()
