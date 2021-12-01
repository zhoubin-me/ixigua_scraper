import time
import os
import re
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

html_url = 'https://www.ixigua.com/embed?group_id=7036308375272948236'

chrome_options = Options()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=chrome_options)
driver.get(html_url)
driver.implicitly_wait(10)
elems = driver.find_elements_by_xpath('//xg-definition/ul/li')
import pdb; pdb.set_trace()
for elem in elems:
    print(elem)
