from selenium.common.exceptions import StaleElementReferenceException, ElementClickInterceptedException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class AccessoriesScreen():
    def __init__(self, driver, config, title):
        self.driver = driver.instance
        self.config = config
        self.section = driver.section
        self.ignored_exceptions = (StaleElementReferenceException, ElementClickInterceptedException,)
        self._validate_breadcrumb(title)

    def _validate_breadcrumb(self, title):
        elements = WebDriverWait(self.driver, 10).until(EC.visibility_of_all_elements_located(
            (By.CSS_SELECTOR, self.config.get(self.section, 'accessories_breadcrumb'))))

        if not ' '.join([element.text for element in elements]) == 'Home > %s' % title:
            raise Exception

    def click_item_left_menu(self, item_name):
        selector = self.config.get(self.section, 'item_left_menu').replace('<replace>', item_name)
        WebDriverWait(self.driver, 10, ignored_exceptions=self.ignored_exceptions).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, selector))).click()
