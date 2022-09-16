from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from shutil import which
import time

CHROME_DRIVER_PATH = which('chromedriver')

options = Options()
options.binary_location = '/Applications/Google Chrome 2.app/Contents/MacOS/Google Chrome'
# options.add_argument('--headless')
driver = webdriver.Chrome(service=Service(CHROME_DRIVER_PATH),
                          options=options)


driver.get('https://duckduckgo.com')

time.sleep(1)
search_box = driver.find_element(By.XPATH, "(//div[@class='searchbox_searchbox__eaWKL']/input)[3]")
search_box.send_keys('My User Agent')
search_box.send_keys(Keys.ENTER)
print(driver.find_element(By.XPATH, '//div[@class="zci__body"]').text)
# print(driver.page_source)
driver.close()
