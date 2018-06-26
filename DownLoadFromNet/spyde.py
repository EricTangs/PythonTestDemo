from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0

browser = webdriver.Chrome()

def search():
    browser.get('https://www.taobao.com')
    try:
        input = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#q")))
        submit = WebDriverWait(browser, 10).until(EC.presence_of_element_located(By.CSS_SELECTOR,"#J_TSearchForm > div.search-button > button"))
    finally:
        browser.quit()