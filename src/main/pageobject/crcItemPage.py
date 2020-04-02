from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from src.main.common.commonPage import CommonClass
from selenium.common.exceptions import StaleElementReferenceException, ElementClickInterceptedException


class SelectedItemScreen(object):
    def __init__(self, driver, config, title, breadcrumb_path):
        CommonClass(driver, config, title, breadcrumb_path)._validate_breadcrumb()
        self.ignored_exceptions = (StaleElementReferenceException, ElementClickInterceptedException,)
        self.driver = driver.instance
        self.config = config
        self.section = driver.section
        self.get_item_page_title()

    def get_item_page_title(self):
        element = WebDriverWait(self.driver, 10, ignored_exceptions=self.ignored_exceptions).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, self.config.get(self.section, 'item_page_title'))))

        return element.text
