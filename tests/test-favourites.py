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
    driver.find_element(By.XPATH, '//*[@id="userName"]')\
        .send_keys('test-user')
    driver.find_element(By.XPATH, '//*[@id="password"]')\
        .send_keys('test')
    driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div/form/button')\
        .click()
    WebDriverWait(driver, 10).until(EC.url_to_be(website_url + "favourites"))
    yield driver


def test_adding_history(logged_in_driver):
    logged_in_driver.get(website_url)

    # Search for dolphin using search bar
    search_input = WebDriverWait(logged_in_driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="basic-navbar-nav"]/form/input')))
    search_input.send_keys('dolphin')
    search_button = WebDriverWait(logged_in_driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="basic-navbar-nav"]/form/button')))
    search_button.click()
    WebDriverWait(logged_in_driver, 10).until(EC.url_to_be(website_url + "artwork?title=true&q=dolphin"))

    # Click on first artwork and wait for page to load
    elements_container = WebDriverWait(logged_in_driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div/div')))
    child_elements = elements_container.find_elements(By.XPATH, './/div')
    first_child_element = child_elements[0]
    first_child_element.find_element(By.XPATH, './/div/div/a/button').click()
    WebDriverWait(logged_in_driver, 10).until(EC.url_to_be(website_url + "artwork/186021"))

    # add artwork to favourites
    favourite_button = WebDriverWait(logged_in_driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div/div/div/div/div/p/button')))
    favourite_button.click()

    # Visit the favorites button by clicking on search history link in dropdown menu
    dropdown_menu = WebDriverWait(logged_in_driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="basic-nav-dropdown"]')))
    dropdown_menu.click()
    favourites_button = WebDriverWait(logged_in_driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="basic-navbar-nav"]/div[2]/div/div/a[1]')))
    favourites_button.click()
    WebDriverWait(logged_in_driver, 10).until(EC.url_to_be(website_url + "favourites"))

    # Check if artwork is in favourites
    initial_favourite_list = logged_in_driver.find_elements(By.XPATH, '//*[@id="__next"]/div/div')
    element = WebDriverWait(logged_in_driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div/div/*[last()]/div/div')))
    text = element.text.split('\n')[0]
    assert text == 'Dolphin'

    # Remove artwork from favourites
    remove_favourite_button = WebDriverWait(logged_in_driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div/div/*[last()]/div/div/a/button')))
    remove_favourite_button.click()
    WebDriverWait(logged_in_driver, 10).until(EC.url_to_be(website_url + "artwork/186021"))
    unfavourite_button = WebDriverWait(logged_in_driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div/div/div/div/div/p/button')))
    unfavourite_button.click()

    # Check if artwork is in favourites
    final_favourite_list = logged_in_driver.find_elements(By.XPATH, '//*[@id="__next"]/div/div')
    assert len(initial_favourite_list) == len(final_favourite_list) + 1, "Favourite was not removed from favourites list"
