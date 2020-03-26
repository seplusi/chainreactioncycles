from selenium.common.exceptions import StaleElementReferenceException, ElementClickInterceptedException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class CommonHomeScreen(object):
    def __init__(self, driver, config):
        self.driver = driver.instance
        self.config = config
        self.section = driver.section
        self.ignored_exceptions = (StaleElementReferenceException, ElementClickInterceptedException,)
        self.get_shop_by_category()

    def get_shop_by_category(self):
        return WebDriverWait(self.driver, 10, ignored_exceptions=self.ignored_exceptions).until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                                         self.config.get(self.section,
                                                                                         'shop_by_category'))))

    def click_shop_by_category_accessories(self, category):
        self.get_shop_by_category().click()
        selector = self.config.get(self.section, 'category_left_menu').replace('<replace>', category)
        WebDriverWait(self.driver, 10, ignored_exceptions=self.ignored_exceptions).until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector))).click()
