from selenium import webdriver
broser = webdriver.Chrome()
broser.get('https://www.taobao.com')
print(broser.page_source)
broser.close()
