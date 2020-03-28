from selenium.common.exceptions import StaleElementReferenceException, ElementClickInterceptedException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time


class HomeScreen(object):
    def __init__(self, driver, config):
        self.driver = driver.instance
        self.config = config
        self.section = driver.section
        self.ignored_exceptions = (StaleElementReferenceException, ElementClickInterceptedException,)
        self.get_shop_by_category()

    def type_text_in_search_box(self, text):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, 'auto_search'))).send_keys(text)

    def click_category_from_search(self, category):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href^='/%s?']" % category))).click()

    def get_shop_by_category(self):
        return WebDriverWait(self.driver, 10, ignored_exceptions=self.ignored_exceptions).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,
                                        self.config.get(self.section,
                                                        'shop_by_category'))))

    def click_shop_by_category_accessories(self, category):
        self.get_shop_by_category().click()
        selector = self.config.get(self.section, 'category_left_menu').replace('<replace>', category)
        WebDriverWait(self.driver, 10, ignored_exceptions=self.ignored_exceptions).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, selector))).click()

    def click_specific_item_from_search(self, item_name):
        elements = WebDriverWait(self.driver, 10, ignored_exceptions=self.ignored_exceptions).until(
            EC.visibility_of_all_elements_located((By.CSS_SELECTOR, self.config.get(self.section, 'item_search_result'))))

        for element in elements:
            if element.text == item_name:
                break
        else:
            print([element.text for element in elements])
            raise Exception

        element.click()
