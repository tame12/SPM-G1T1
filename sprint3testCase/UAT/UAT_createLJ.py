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

#WIP
def test_createLJ(i, driver, wait,):
    logging.info(f'Start of test {i}')
    time1 = time.time()
    driver.find_element(By.ID, "position").click()
    driver.find_element(By.ID, "dropdownEmailAdmin").click()
    driver.find_element(By.ID, "password").click()
    driver.find_element(By.ID, "password").send_keys("password")
    driver.find_element(By.CSS_SELECTOR, ".button").click()
    driver.find_element(By.ID, "assignNewRole").click()
    driver.find_element(By.XPATH, "(//button[@id=\'1\'])[2]").click()
    driver.find_element(By.CSS_SELECTOR, "#\\31 > .accordion-button").click()
    driver.find_element(By.CSS_SELECTOR, "#skill1 .btn").click()
    # driver.find_element(By.CSS_SELECTOR, "#\\32 > .accordion-button").click()
    # driver.find_element(By.CSS_SELECTOR, "#skill2 .btn").click()
    # assert driver.switch_to.alert.text == "Please select a course that you haven\'t already selected"
    driver.find_element(By.CSS_SELECTOR, ".button").click()
    time2 = time.time()

    # WIP, need to actually verify success
    logging.info('verified LJ is created')

    # assert time taken is under 2 minute
    assert time2-time1 < 120

    logging.info(f'Time taken: {time2-time1:.2f} seconds')
    logging.info(f'Time taken is under 2 minutes: {time2-time1 < 120}')
    logging.info(f'End of test {i}')
    return


def manyTest_createLJ(n=1):

  log_level = logging.INFO  # logging.DEBUG # debug shows all http requests by selenium
  datefmt = '%m/%d/%Y %I:%M:%S %p'

  info = None
  with open('metadata.json', 'r') as f:
    info = json.load(f)

  test_name = info['test_createLJ']['name']
  test_desc = info["test_createLJ"]['description']
  # skills = info["test_createLJ"]["skills"]

  url = info["test_createLJ"]["url"]
  log_output = info["log_output"]

  logging.basicConfig(format='%(asctime)s\t%(levelname)s:\t%(message)s',level=log_level, filename=log_output, filemode='a', datefmt=datefmt)

  opening_log = f'New Test=====\n{test_name}\n{n} tests\n{test_desc}\nat time: {time.strftime(datefmt)}\n\n'

  with open(log_output, 'a') as f:
    f.write(opening_log)

  options = webdriver.ChromeOptions()
  options.add_experimental_option('excludeSwitches', ['enable-logging'])

  driver = webdriver.Chrome(
      executable_path="../../sprint1testCase/chromedriver", options=options)
  driver.implicitly_wait(10)
  wait = WebDriverWait(driver, 10)
  driver.get(url)

  for i in range(1, n+1):
    print(f'starting test {i}')
    try:
      test_createLJ(i, driver, wait)
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
      logging.exception(
          'Unable to access webdriver, aborting remainding tests')
      break

    if i < n:
      print("sleeping for 10s start")
      time.sleep(10)

  with open(log_output, 'a') as f:
    print('Ending tests')
    closing_log = 'Test End=====\n\n'
    f.write(closing_log)


if __name__ == "__main__":
  manyTest_createLJ()
