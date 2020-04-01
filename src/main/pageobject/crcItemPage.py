from selenium.common.exceptions import StaleElementReferenceException, ElementClickInterceptedException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class SelectedItemScreen():
    def __init__(self, driver, config, title, breadcrumb_path):
        self.driver = driver.instance
        self.config = config
        self.section = driver.section
        self.ignored_exceptions = (StaleElementReferenceException, ElementClickInterceptedException,)
        self.title = title
        self.breadcrumb_path = breadcrumb_path
        self._validate_breadcrumb()

    def _validate_breadcrumb(self):
        elements = WebDriverWait(self.driver, 10).until(EC.visibility_of_all_elements_located(
            (By.CSS_SELECTOR, self.config.get(self.section, 'accessories_breadcrumb'))))

        if not ' '.join([element.text for element in elements]) == '%s %s' % (self.breadcrumb_path, self.title):
            raise Exception

    def get_item_page_title(self):
        element = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, 'li.crcPDPTitle > h1')))

        return element.text
