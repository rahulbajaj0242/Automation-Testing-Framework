import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
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


def test_navbar_links_unauthenticated(driver):
  driver.get(website_url)

  # Test register button
  register_button = driver.find_element(By.XPATH, '//*[@id="basic-navbar-nav"]/div[2]/a[1]')
  register_button.click()
  WebDriverWait(driver, 10).until(EC.url_to_be(website_url + "register"))
  assert driver.current_url == (website_url + "register"), "Expected URL to be {} but got {}".format(website_url + "register", driver.current_url)

  # Test login button
  login_button = driver.find_element(By.XPATH, '//*[@id="basic-navbar-nav"]/div[2]/a[2]')
  login_button.click()
  WebDriverWait(driver, 10).until(EC.url_to_be(website_url + "login"))
  assert driver.current_url == (website_url + "login"), "Expected URL to be {} but got {}".format(website_url + "login", driver.current_url)

  # Test home button
  home_button = driver.find_element(By.XPATH, '//*[@id="basic-navbar-nav"]/div[1]/a')
  home_button.click()
  WebDriverWait(driver, 10).until(EC.url_to_be(website_url))
  assert driver.current_url == (website_url), "Expected URL to be {} but got {}".format(website_url, driver.current_url)


def test_navbar_links_authenticated(logged_in_driver):
  logged_in_driver.get(website_url)

  # Test advanced search button
  advanced_search_button = logged_in_driver.find_element(By.XPATH, '//*[@id="basic-navbar-nav"]/div[1]/a[2]')
  advanced_search_button.click()
  WebDriverWait(logged_in_driver, 10).until(EC.url_to_be(website_url + "search"))
  assert logged_in_driver.current_url == (website_url + "search"), "Expected URL to be {} but got {}".format(website_url + "search", logged_in_driver.current_url)

  # test quick search form
  search_input = logged_in_driver.find_element(By.XPATH, '//*[@id="basic-navbar-nav"]/form/input')
  search_input.send_keys('dolphin')
  search_button = logged_in_driver.find_element(By.XPATH, '//*[@id="basic-navbar-nav"]/form/button')
  search_button.click()
  WebDriverWait(logged_in_driver, 10).until(EC.url_to_be(website_url + "artwork?title=true&q=dolphin"))
  assert logged_in_driver.current_url == (website_url + "artwork?title=true&q=dolphin"), "Expected URL to be {} but got {}".format(website_url + "artwork?title=true&q=dolphin", logged_in_driver.current_url)

  # test dropdown menu
  dropdown_menu = logged_in_driver.find_element(By.XPATH, '//*[@id="basic-nav-dropdown"]')
  dropdown_menu.click()
  logged_in_driver.implicitly_wait(2)

  # test favourites button in dropdown menu
  favourites_button = logged_in_driver.find_element(By.XPATH, '//*[@id="basic-navbar-nav"]/div[2]/div/div/a[1]')
  favourites_button.click()
  WebDriverWait(logged_in_driver, 10).until(EC.url_to_be(website_url + "favourites"))
  assert logged_in_driver.current_url == (website_url + "favourites"), "Expected URL to be {} but got {}".format(website_url + "favourites", logged_in_driver.current_url)

  # test history button in dropdown menu 
  dropdown_menu.click()
  history_button = logged_in_driver.find_element(By.XPATH, '//*[@id="basic-navbar-nav"]/div[2]/div/div/a[2]')
  history_button.click()
  WebDriverWait(logged_in_driver, 10).until(EC.url_to_be(website_url + "history"))
  assert logged_in_driver.current_url == (website_url + "history"), "Expected URL to be {} but got {}".format(website_url + "history", logged_in_driver.current_url)

  # test logout button in dropdown menu
  dropdown_menu.click()
  logout_button = logged_in_driver.find_element(By.XPATH, '//*[@id="basic-navbar-nav"]/div[2]/div/div/a[3]')
  logout_button.click()
  WebDriverWait(logged_in_driver, 10).until(EC.url_to_be(website_url + "login"))
  assert logged_in_driver.current_url == (website_url + "login"), "Expected URL to be {} but got {}".format(website_url + "login", logged_in_driver.current_url)

