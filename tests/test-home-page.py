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

@pytest.fixture
def logged_in_driver(driver):
  driver.get(website_url + "login")
  driver.find_element(By.XPATH, '//*[@id="userName"]').send_keys('test-user')
  driver.find_element(By.XPATH, '//*[@id="password"]').send_keys('test')
  driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div/form/button').click()
  WebDriverWait(driver, 10).until(EC.url_to_be(website_url + "favourites"))
  yield driver


# Test cases for search home button
def test_home_search_button_unauthenticated(driver):
  driver.get(website_url)
  driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div/button').click()
  print(driver.current_url)
  WebDriverWait(driver, 10).until(EC.url_to_be(website_url + "login"))
  assert driver.current_url == (website_url + "login")

def test_home_search_button_authenticated(logged_in_driver):
  logged_in_driver.get(website_url)
  logged_in_driver.find_element(By.XPATH, '//*[@id="basic-navbar-nav"]/div[1]/a[1]').click()
  logged_in_driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div/button').click()
  WebDriverWait(logged_in_driver, 10).until(EC.url_to_be(website_url + "search"))
  assert logged_in_driver.current_url == (website_url + "search")

