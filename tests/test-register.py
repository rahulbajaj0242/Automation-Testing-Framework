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
def test_successful_register(driver):
  pass