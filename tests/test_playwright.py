import pytest
from playwright.sync_api import sync_playwright

def test_playwright_google():
    """Test basic Playwright functionality"""
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=[
                '--no-sandbox',
                '--disable-dev-shm-usage',
                '--disable-gpu',
                '--single-process'
            ]
        )
        page = browser.new_page()
        page.goto('https://www.google.com')
        
        assert 'Google' in page.title()
        print(f"✓ Playwright test passed - Page title: {page.title()}")
        
        browser.close()

def test_playwright_example():
    """Test Playwright navigation and selectors"""
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=[
                '--no-sandbox',
                '--disable-dev-shm-usage',
                '--disable-gpu',
                '--single-process'
            ]
        )
        page = browser.new_page()
        page.goto('https://example.com')
        
        assert 'Example Domain' in page.title()
        h1_text = page.locator('h1').text_content()
        assert h1_text == 'Example Domain'
        print("✓ Playwright element test passed")
        
        browser.close()
