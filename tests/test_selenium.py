import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

def get_chrome_options():
    """Configure Chrome options for Lambda environment"""
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--single-process')
    chrome_options.binary_location = '/usr/bin/google-chrome'
    return chrome_options

def test_google_search():
    """Test basic Selenium functionality"""
    service = Service(executable_path='/usr/local/bin/chromedriver')
    driver = webdriver.Chrome(service=service, options=get_chrome_options())
    
    try:
        driver.get('https://www.google.com')
        assert 'Google' in driver.title
        print(f"✓ Selenium test passed - Page title: {driver.title}")
    finally:
        driver.quit()

def test_example_website():
    """Test navigation and element finding"""
    service = Service(executable_path='/usr/local/bin/chromedriver')
    driver = webdriver.Chrome(service=service, options=get_chrome_options())
    
    try:
        driver.get('https://example.com')
        assert 'Example Domain' in driver.title
        h1 = driver.find_element(By.TAG_NAME, 'h1')
        assert h1.text == 'Example Domain'
        print("✓ Selenium element test passed")
    finally:
        driver.quit()
