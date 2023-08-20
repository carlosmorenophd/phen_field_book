from selenium import webdriver

DRIVER_PATH = '/usr/bin/google-chrome'
driver = webdriver.Chrome('../google-chrome/chromedriver_114/chromedriver')

driver.get('https://google.com')

