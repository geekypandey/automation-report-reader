import csv

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException

from helper import list_actions

# DIR='/home/bruhh/workspace/bmc/html_reports/automation/HTML_20Report'
DIR='/home/bruhh/workspace/bmc/html_reports/automation/html_r'

STATUS='/html/body/div[2]/div[1]/section/div/div[1]/a'
FAIL='/html/body/div[2]/div[1]/section/div/div[1]/ul/li[2]'

fields = ['test-name', 'test-status', 'test-time', 'test-author']


driver = webdriver.Chrome()
driver.get(f'file://{DIR}/report.html')

action = ActionChains(driver)

# select all fail status
s = driver.find_element_by_xpath(STATUS)
action.move_to_element(s).perform()
s = driver.find_element_by_xpath(FAIL)
action.move_to_element(s).perform()
s.click()

lst = driver.find_element_by_id('test-collection')
d = lst.find_elements_by_class_name('test-heading')
action = ActionChains(driver)


for row in d:
    if row.is_displayed():
        action.move_to_element(row).perform()
        row.click()
        for f in fields:
            try:
                ele = row.find_element_by_class_name(f)
                print(f'{f}: {ele.text}')
            except NoSuchElementException:
                print(f'{f}: NULL')
        table = driver.find_elements_by_css_selector("tr.log[status='fail']")
        table = [i for i in table if i.is_displayed()]
        table = table[1:3]
        f, s = table
        f = f.text.split(' ',maxsplit=3)[1:]
        t = ' '.join(f[:2])
        code, desc = f[2].split(maxsplit=1)
        print('time:', t)
        print(code, desc)
        print('error:', s.text.split(maxsplit=3)[3])
        print('')

driver.close()
