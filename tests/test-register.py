import time
import pytest
import uuid
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

@pytest.fixture
def unique_username():
    yield 'user' + str(uuid.uuid4().hex)[:8] 


# Test cases for register form
def test_successful_register(driver, unique_username):
  driver.get(webiste_url + "register")
  driver.find_element(By.XPATH, '//*[@id="userName"]').send_keys(unique_username)
  driver.find_element(By.XPATH, '//*[@id="password"]').send_keys("test")
  driver.find_element(By.XPATH, '//*[@id="confirmPassword"]').send_keys("test")
  driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div/form/button').click()
  time.sleep(3)
  assert driver.current_url == (webiste_url + "login")

def test_unsuccessful_register_username_exist(driver):
  driver.get(webiste_url + "register")
  driver.find_element(By.XPATH, '//*[@id="userName"]').send_keys('test-user')
  driver.find_element(By.XPATH, '//*[@id="password"]').send_keys("test")
  driver.find_element(By.XPATH, '//*[@id="confirmPassword"]').send_keys("test")
  driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div/form/button').click()
  time.sleep(1)
  alert_text = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div/form/div[4]/div[2]').text
  assert alert_text == "User Name already taken"

def test_unsuccessful_register_password_not_match(driver, unique_username):
  driver.get(webiste_url + "register")
  driver.find_element(By.XPATH, '//*[@id="userName"]').send_keys(unique_username)
  driver.find_element(By.XPATH, '//*[@id="password"]').send_keys("test")
  driver.find_element(By.XPATH, '//*[@id="confirmPassword"]').send_keys("tes")
  driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div/form/button').click()
  time.sleep(1)
  alert_text = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div/form/div[4]/div[2]').text
  assert alert_text == "Passwords do not match"