from selenium.common.exceptions import StaleElementReferenceException, ElementClickInterceptedException, TimeoutException, ElementNotVisibleException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class searchResultScreen(object):
    def __init__(self, driver, config, breadcrum_sub_path):
        self.driver = driver.instance
        self.config = config
        self.section = driver.section
        self.ignored_exceptions = (StaleElementReferenceException, ElementClickInterceptedException, ElementNotVisibleException, )
        self._validate_breadcrumb(breadcrum_sub_path)

    def _validate_breadcrumb(self, breadcrum_sub_path):
        elements = WebDriverWait(self.driver, 10).until(EC.visibility_of_all_elements_located(
            (By.CSS_SELECTOR, self.config.get(self.section, 'accessories_breadcrumb'))))

        if not ' '.join([element.text for element in elements]) == 'Home > %s' % breadcrum_sub_path:
            raise Exception

    def click_item(self, item_name):
        selector = self.config.get(self.section, 'search_item_with_name').replace('<replace>', '%s' % item_name)
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector))).click()
