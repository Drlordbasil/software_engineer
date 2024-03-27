import unittest
from browser_automation.browser import Browser

class TestBrowserAutomation(unittest.TestCase):
    def setUp(self):
        self.browser = Browser()

    def tearDown(self):
        self.browser.quit()

    def test_navigation(self):
        self.browser.navigate("https://www.example.com")
        self.assertIn("Example", self.browser.driver.title)

    def test_click(self):
        self.browser.navigate("https://www.example.com")
        self.browser.click("a.example-link")
        self.assertIn("example-page", self.browser.driver.current_url)

    def test_type(self):
        self.browser.navigate("https://www.example.com/form")
        self.browser.type("input[name='username']", "testuser")
        self.browser.type("input[name='password']", "testpassword")
        self.browser.click("button[type='submit']")
        self.assertIn("Welcome, testuser", self.browser.driver.page_source)

if __name__ == "__main__":
    unittest.main()