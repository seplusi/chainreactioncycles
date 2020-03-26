from selenium.common.exceptions import StaleElementReferenceException, ElementClickInterceptedException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class SelectedItemScreen():
    def __init__(self, driver, config, title):
        self.driver = driver.instance
        self.config = config
        self.section = driver.section
        self.ignored_exceptions = (StaleElementReferenceException, ElementClickInterceptedException,)
        self.title = title

    def get_item_page_title(self):
        element = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, 'li.crcPDPTitle > h1')))

        return element.text
