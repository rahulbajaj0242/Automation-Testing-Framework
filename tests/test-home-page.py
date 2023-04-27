import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert

webiste_url = "https://museum-app-sandy.vercel.app/"

# Setting up selenium driver
@pytest.fixture
def driver():
  driver = webdriver.Chrome()
  yield driver
  driver.quit()


# Test cases for search home button
def test_home_search_button_unauthenticated(driver):
  driver.get(webiste_url)
  driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div/button').click()
  print(driver.current_url)
  time.sleep(1)
  assert driver.current_url == (webiste_url + "login")

