from selenium.common.exceptions import StaleElementReferenceException, ElementClickInterceptedException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time


class CommonClass(object):
    def __init__(self, driver, config, title=None, breadcrumb_path=None):
        self.driver = driver.instance
        self.config = config
        self.section = driver.section
        self.ignored_exceptions = (StaleElementReferenceException, ElementClickInterceptedException,)
        self.title = title
        self.breadcrumb_path = breadcrumb_path

    def _validate_breadcrumb(self, timeout=10):
        for _ in range(timeout):
            elements = WebDriverWait(self.driver, 10).until(EC.visibility_of_all_elements_located(
                (By.CSS_SELECTOR, self.config.get(self.section, 'accessories_breadcrumb'))))

            if self.title == '':
                bread_crumb = self.breadcrumb_path
            else:
                bread_crumb = '%s %s' % (self.breadcrumb_path, self.title)

            if not ' '.join([element.text for element in elements]) == bread_crumb:
                time.sleep(1)
            else:
                break
        else:
            print('Could not find breadcrumb %s' % bread_crumb)
            raise Exception

    def validate_heading(self, timeout=10):
        for _ in range(timeout):
            element = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(
                (By.CSS_SELECTOR, self.config.get(self.section, 'page_heading'))))
            if element.text == self.title:
                break
            else:
                time.sleep(1)
        else:
            print('Could not find heading %s' % self.title)
            raise Exception
