import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

webiste_url = "https://museum-app-sandy.vercel.app/"

# Setting up selenium driver
@pytest.fixture
def driver():
  driver = webdriver.Chrome()
  yield driver
  driver.quit()

def test_home_search_button_unauthenticated(driver):
  driver.get(webiste_url)
  driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div/button').click()
  print(driver.current_url)
  time.sleep(1)
  assert driver.current_url == (webiste_url + "login")

def test_successful_log_in(driver):
  driver.get(webiste_url + "login")
  time.sleep(1)
  driver.find_element(By.XPATH, '//*[@id="userName"]').send_keys('test-user')
  driver.find_element(By.XPATH, '//*[@id="password"]').send_keys('test')
  driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div/form/button').click()
  time.sleep(5)
  assert driver.current_url == (webiste_url + "favourites")