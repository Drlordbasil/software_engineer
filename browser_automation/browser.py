from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .utils import scroll_to_element, wait_for_element
import logging

logger = logging.getLogger(__name__)

class Browser:
    def __init__(self):
        self.driver = webdriver.Chrome()
        logger.info("Browser initialized.")

    def navigate(self, url):
        self.driver.get(url)
        logger.info(f"Navigated to: {url}")

    def click(self, selector):
        element = wait_for_element(self, selector)
        if element:
            element.click()
            logger.info(f"Clicked element: {selector}")
        else:
            logger.warning(f"Element not found for clicking: {selector}")

    def type(self, selector, text):
        element = wait_for_element(self, selector)
        if element:
            element.send_keys(text)
            logger.info(f"Typed '{text}' into element: {selector}")
        else:
            logger.warning(f"Element not found for typing: {selector}")

    def scroll_to(self, selector):
        scroll_to_element(self, selector)

    def quit(self):
        self.driver.quit()
        logger.info("Browser quit.")