import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

website_url = "https://museum-app-sandy.vercel.app/"

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
def test_adding_history(logged_in_driver): 
  logged_in_driver.get(website_url)

  # Search for dolphin using search bar
  search_input = logged_in_driver.find_element(By.XPATH, '//*[@id="basic-navbar-nav"]/form/input')
  search_input.send_keys('dolphin')
  search_button = logged_in_driver.find_element(By.XPATH, '//*[@id="basic-navbar-nav"]/form/button')
  search_button.click()
  WebDriverWait(logged_in_driver, 10).until(EC.url_to_be(website_url + "artwork?title=true&q=dolphin"))

  # Visit the history button by clicking on search history link in dropdown menu
  dropdown_menu = logged_in_driver.find_element(By.XPATH, '//*[@id="basic-nav-dropdown"]')
  dropdown_menu.click()
  logged_in_driver.implicitly_wait(2)
  history_button = logged_in_driver.find_element(By.XPATH, '//*[@id="basic-navbar-nav"]/div[2]/div/div/a[2]')
  history_button.click()
  WebDriverWait(logged_in_driver, 10).until(EC.url_to_be(website_url + "history"))

  # Check that history contains the dolphin search
  history_container = logged_in_driver.find_element(By.XPATH, '//*[@id="__next"]/div/div')
  history_elements = history_container.find_elements(By.XPATH, './/div')
  last_history_element = history_elements[-1]
  assert "dolphin" in last_history_element.text, "Expected 'dolphin' to be in the last div's text content (lastest history element), but it was not found."

  # delete 'dolphin' from history
  delete_button = last_history_element.find_element(By.XPATH, './/button')
  delete_button.click()

  # Wait for the history element to be deleted
  WebDriverWait(logged_in_driver, 10).until(EC.staleness_of(last_history_element))

  # Check that the history element is deleted
  new_history_container = logged_in_driver.find_element(By.XPATH, '//*[@id="__next"]/div/div')
  new_history_elements = new_history_container.find_elements(By.XPATH, './/div')
  assert len(new_history_elements) == len(history_elements) - 1, "Expected the number of history elements to decrease by 1, but it did not."

