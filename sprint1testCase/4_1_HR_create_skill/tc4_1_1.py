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



def tc4_1_1(i, driver, wait):

  logging.info(f'Start of test {i}')
  timings = []

  driver.find_element(By.CSS_SELECTOR, ".button-primary:nth-child(1)").click()
  uniqueSkillName = f'uniqueskillname {time.time()}'[:50] # max length of skill name is 50
  time.sleep(1)  # selenium is too fast
  driver.find_element(By.ID, "create_skill_input").send_keys(uniqueSkillName)
  time.sleep(1) # selenium is too fast

  logging.info('before clicking create skill button')
  timings.append(time.time())

  driver.find_element(By.ID, "create_skill_button").click()

  #green box with text "Skill created successfully."
  # EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#view-results > *:last-child > *:nth-child(1)"), uniqueSkillName)
  wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#error_success_bar > div"), "Skill created successfully."))

  #new skill is in the list of skills
  assert driver.find_element(By.NAME, uniqueSkillName).text == uniqueSkillName

  logging.info('verified the creation of skill') 
  timings.append(time.time())

  logging.info(f'End of test {i}')
  logging.info(f'Time taken for to post and verify skill: {timings[1]-timings[0]}')
  return



def manytc4_1_1(n = 1):

  log_level = logging.INFO # logging.DEBUG # debug shows all http requests by selenium
  datefmt = '%m/%d/%Y %I:%M:%S %p'
  
  info = None
  with open('metadata.json','r') as f:
    info = json.load(f)

  test_name = info['tc4_1_1']['name']
  test_desc = info["tc4_1_1"]['description']

  url = info["tc4_1_1"]["url"]
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
      tc4_1_1(i, driver, wait)
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
  manytc4_1_1()
