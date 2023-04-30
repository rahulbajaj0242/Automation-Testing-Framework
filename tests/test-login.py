import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

website_url = "https://artexplorer-pro.vercel.app/"

# Setting up selenium driver
@pytest.fixture
def driver():
  driver = webdriver.Chrome()
  yield driver
  driver.quit()


# Test cases for login form
def test_successful_log_in(driver):
  driver.get(website_url + "login")
  driver.find_element(By.XPATH, '//*[@id="userName"]').send_keys('test-user')
  driver.find_element(By.XPATH, '//*[@id="password"]').send_keys('test')
  driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div/form/button').click()
  WebDriverWait(driver, 10).until(EC.url_to_be(website_url + "favourites"))
  assert driver.current_url == (website_url + "favourites")

def test_unsuccessful_log_in_wrong_userName(driver):
  driver.get(website_url + "login")
  driver.find_element(By.XPATH, '//*[@id="userName"]').send_keys('wrong-username')
  driver.find_element(By.XPATH, '//*[@id="password"]').send_keys('test')
  driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div/form/button').click()
  driver.implicitly_wait(5)
  alert_text = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div/form/div[3]/div[2]').text
  assert alert_text == "Unable to find user wrong-username"

def test_unsuccessful_log_in_wrong_password(driver):
  driver.get(website_url + "login")
  driver.find_element(By.XPATH, '//*[@id="userName"]').send_keys('test-user')
  driver.find_element(By.XPATH, '//*[@id="password"]').send_keys('wrong-password')
  driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div/form/button').click()
  driver.implicitly_wait(5)
  alert_text = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div/form/div[3]/div[2]').text
  assert alert_text == "Incorrect password for user test-user"
