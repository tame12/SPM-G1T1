import pytest
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import logging



def tc4_2_1(i, driver, wait, skills):

  logging.info(f'Start of test {i}')

  #new skill is in the list of skills
  assert driver.find_element(By.ID, "1").text == skills["1"]
  assert driver.find_element(By.ID, "2").text == skills["2"]
  assert driver.find_element(By.ID, "3").text == skills["3"]

  logging.info('verified the skill can be viewed') 

  logging.info(f'End of test {i}')
  return



def manytc4_2_1(n = 1):

  log_level = logging.INFO # logging.DEBUG # debug shows all http requests by selenium
  datefmt = '%m/%d/%Y %I:%M:%S %p'
  
  info = None
  with open('metadata.json','r') as f:
    info = json.load(f)

  test_name = info['tc4_2_1']['name']
  test_desc = info["tc4_2_1"]['description']
  skills = info["tc4_2_1"]["skills"]

  url = info["tc4_2_1"]["url"]
  log_output = info["log_output"]

  logging.basicConfig(format='%(asctime)s\t%(levelname)s:\t%(message)s', level=log_level, filename=log_output, filemode='a', datefmt=datefmt)

  opening_log = f'New Test=====\n{test_name}\n{n} tests\n{test_desc}\nat time: {time.strftime(datefmt)}\n\n'

  with open(log_output,'a') as f:
    f.write(opening_log)

  options = webdriver.ChromeOptions()
  options.add_experimental_option('excludeSwitches', ['enable-logging'])

  driver = webdriver.Chrome(executable_path="../chromedriver", options=options)
  driver.implicitly_wait(10)
  wait = WebDriverWait(driver, 10)
  driver.get(url)

  for i in range(1,n+1):
    print(f'starting test {i}')
    try:
      tc4_2_1(i, driver, wait, skills)
      print(f'ending test {i}')
    except Exception as e:
      print(f'Test {i} error, continuing with next test')
      logging.exception(f'Test {i} error, continuing with next test')
      logging.exception(e)
      pass
  
    try:
      driver.get(url)
    except Exception:
      print('Unable to access webdriver, aborting remainding tests')
      logging.exception('Unable to access webdriver, aborting remainding tests')
      break
    
    if i < n:
      print("sleeping for 10s start")
      time.sleep(10)

  with open(log_output, 'a') as f:
    print('Ending tests')
    closing_log = 'Test End=====\n\n'
    f.write(closing_log)


if __name__ == "__main__":
  manytc4_2_1()
