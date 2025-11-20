import json
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

def handler(event, context):
    """
    AWS Lambda handler to run Selenium tests
    """
    test_type = event.get('test_type', 'selenium')  # 'selenium' or 'playwright'
    
    if test_type == 'selenium':
        return run_selenium_test()
    elif test_type == 'playwright':
        return run_playwright_test()
    else:
        return {
            'statusCode': 400,
            'body': json.dumps('Invalid test_type. Use "selenium" or "playwright"')
        }

def run_selenium_test():
    """Run a simple Selenium test"""
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--single-process')
    chrome_options.add_argument('--disable-dev-tools')
    chrome_options.add_argument('--no-zygote')
    chrome_options.binary_location = '/usr/bin/google-chrome'
    
    service = Service(executable_path='/usr/local/bin/chromedriver')
    
    try:
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get('https://www.google.com')
        title = driver.title
        driver.quit()
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'test_type': 'selenium',
                'status': 'success',
                'page_title': title
            })
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'test_type': 'selenium',
                'status': 'error',
                'error': str(e)
            })
        }

def run_playwright_test():
    """Run pytest with Playwright tests"""
    try:
        result = subprocess.run(
            ['pytest', 'tests/test_playwright.py', '-v'],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'test_type': 'playwright',
                'status': 'success' if result.returncode == 0 else 'failed',
                'output': result.stdout,
                'errors': result.stderr
            })
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'test_type': 'playwright',
                'status': 'error',
                'error': str(e)
            })
        }
