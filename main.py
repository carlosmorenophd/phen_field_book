from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import re

def process_item(actions, driver, link_to_work):
    print(link_to_work.get_attribute("href"))
    actions.move_to_element(link_to_work)
    actions.click(link_to_work)
    actions.perform()
    tr_tags = list(filter(lambda tag: not re.search('None', str(tag.get_attribute("data-rk"))), driver.find_elements(By.TAG_NAME, 'tr') ))
    for tr_tag in tr_tags:
        print(tr_tag.get_attribute('data-rk'))
        a_tags = list(filter(lambda tag: re.search('Access File', str(tag.get_attribute("data-original-title"))), tr_tag.find_elements(By.TAG_NAME, 'a') ))
        for a_tag in a_tags:
            print('Class',a_tag.get_attribute('class'))
            actions.move_to_element(a_tag)
            actions.click(a_tag)
            actions.perform()
            ul_tag = driver.find_element(By.XPATH, "//ul[@class='dropdown-menu pull-right text-left']")
            a_ul_tag=ul_tag.find_element(By.XPATH, "//a[@class='ui-commandlink ui-widget btn-download']")
            print("Button to download file", a_ul_tag.get_attribute("id"))
            # actions.move_to_element(a_ul_tag)
            # actions.click(a_ul_tag)
            # actions.perform()
            
            # for ul_tag in ul_tags:
            #     a_ul_tags = list(filter(lambda tag: not re.search('#', str(tag.get_attribute("href"))), ul_tag.find_elements(By.TAG_NAME, 'a') ))
            #     for a_ul_tag in a_ul_tags:
            #         print(a_ul_tag.get_attribute('id'))
            #         actions.move_to_element(a_ul_tag)
            #         actions.click(a_ul_tag)
            #         actions.perform()
            #         button_accept=driver.find_element(By.XPATH, "//button[@id='datasetForm:j_idt2273']")
            #         print(button_accept.text)
                    # actions.move_to_element(button_accept)
                    # actions.click(button_accept)
                    # actions.perform()
 
 
            # class=""
    driver.back()    

service = Service(executable_path='../google-chrome/chromedriver_114/chromedriver')
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)
driver.get('https://data.cimmyt.org/dataverse/root')
actions = ActionChains(driver=driver, duration=250)

link_tag_documents = list(filter(lambda link: re.search('/dataset.xhtml', str(link.get_attribute("href"))),driver.find_elements(By.TAG_NAME, 'a') ))
process_item(driver=driver, actions=actions, link_to_work=link_tag_documents[0])


# for link in link_tag_documents:
#     print(link.get_attribute("href"))
driver.quit()




