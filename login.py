from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.common.exceptions import TimeoutException
import time

BASE_DIR = Path(__file__).resolve().parent
WORKSPACE_DIR = BASE_DIR.parent
PROFILE_DIR = BASE_DIR / "selenium_chrome_profile"
STEALTH_JS = BASE_DIR / "stealth.min.js"
if not STEALTH_JS.exists():
    STEALTH_JS = WORKSPACE_DIR / "stealth.min.js"

options = Options()
options.add_argument(f"--user-data-dir={PROFILE_DIR}")

driver = webdriver.Chrome(options=options)
wait_10s = WebDriverWait(driver, 10)
wait_2m = WebDriverWait(driver, 120)

with open(STEALTH_JS, encoding="utf-8") as f:
    js = f.read()
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": js})

try:
    driver.get("https://www.bilibili.com/")

    try:
        wait_10s.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="app"]/div[2]/div[1]/div[1]/ul[2]/li[1]/li/div[1]/div/span')))
        time.sleep(0.3)
        login_bottom = driver.find_element(By.XPATH, '//*[@id="app"]/div[2]/div[1]/div[1]/ul[2]/li[1]/li/div[1]/div/span')
        ActionChains(driver).move_to_element(login_bottom).perform()
        
        wait_10s.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div[1]/div[1]/ul[2]/li[1]/li/div[2]/div/div/div[2]')))
        time.sleep(0.1)
        login_immediately = driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div[1]/div[1]/ul[2]/li[1]/li/div[2]/div/div/div[2]')
        ActionChains(driver).move_to_element(login_immediately).perform()
        ActionChains(driver).click(login_immediately).perform()

        timer = 0
        while timer <= 60:
            try:
                wait_10s.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[3]/div')))
            except TimeoutException:
                break
            time.sleep(0.1)
            timer += 0.1

        if timer > 60:
            print ("please scan QR and login first")
        else:
            print ("login succesfully, please run message.py to scrape message")
        
    except TimeoutException:
        print ("you have already login, please run message.py to scrape message")

except TimeoutException:
    print ("encountered some errors, please check the error messages on the browser.")
    time.sleep(28.5)

finally:
    time.sleep(1.5)
    driver.quit()
