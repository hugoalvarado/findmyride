from selenium import webdriver

#used Chrome webdriver from http://chromedriver.storage.googleapis.com/index.html?path=2.27/
browser = webdriver.Chrome()
browser.get('http://localhost:8000')

assert 'Django' in browser.title