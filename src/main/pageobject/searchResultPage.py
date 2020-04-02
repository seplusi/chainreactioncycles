from selenium.common.exceptions import StaleElementReferenceException, ElementClickInterceptedException, ElementNotVisibleException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from src.main.common.commonPage import CommonClass
import time
import re


class searchResultScreen(CommonClass):
    def __init__(self, driver, config, title, breadcrumb_sub_path):
        super().__init__(driver, config, title, breadcrumb_sub_path)
        self.title = 'Search Results for "%s"' % title
        self.ignored_exceptions = (StaleElementReferenceException, ElementClickInterceptedException, ElementNotVisibleException, )
        self._validate_breadcrumb()
        self.validate_heading(title)

    def validate_heading(self, title, timeout=10):
        for _ in range(timeout):
            element = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(
                (By.ID, self.config.get(self.section, 'search_results_heading'))))
            if re.search("^[0-9]+ results for '%s'" % title, element.text):
                break
            else:
                time.sleep(1)
        else:
            print('Could not find heading %s' % self.title)
            raise Exception

    def click_item(self, item_name):
        selector = self.config.get(self.section, 'search_item_with_name').replace('<replace>', '%s' % item_name)
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector))).click()
