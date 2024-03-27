import logging
from selenium.common.exceptions import NoSuchElementException, TimeoutException

logger = logging.getLogger(__name__)

def scroll_to_element(browser, selector):
    try:
        element = browser.driver.find_element_by_css_selector(selector)
        browser.driver.execute_script("arguments[0].scrollIntoView();", element)
        logger.info(f"Scrolled to element: {selector}")
    except NoSuchElementException:
        logger.warning(f"Element not found: {selector}")

def wait_for_element(browser, selector, timeout=10):
    try:
        element = WebDriverWait(browser.driver, timeout).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, selector))
        )
        logger.info(f"Element found: {selector}")
        return element
    except TimeoutException:
        logger.warning(f"Element not found within timeout: {selector}")
        return None