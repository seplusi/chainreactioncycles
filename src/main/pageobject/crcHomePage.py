from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException, ElementClickInterceptedException
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

    def type_text_in_search_box(self, text):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, 'auto_search'))).send_keys(text)

    def get_search_items_list(self):
        elements = WebDriverWait(self.driver, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'li.ui-menu-item > a > span')))

        return [element.text for element in elements]

    def click_see_all_results(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'span.see-all'))).click()


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

        # Make sure category was expanded
        for _ in range(2):
            try:
                WebDriverWait(self.driver, 10, ignored_exceptions=self.ignored_exceptions).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, 'li.level.level1.active_category > span')))
                break
            except TimeoutException:
                print('Category %s wasn\'t successfully clicked. Going for another stab' % category)
                WebDriverWait(self.driver, 10, ignored_exceptions=self.ignored_exceptions).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, selector))).click()
        else:
            raise Exception

    def click_specific_item_from_search(self, item_name):
        elements = WebDriverWait(self.driver, 10, ignored_exceptions=self.ignored_exceptions).until(
            EC.visibility_of_all_elements_located((By.CSS_SELECTOR, self.config.get(self.section, 'item_search_result'))))

        for element in elements:
            if element.text.lower() == item_name.lower():
                break
        else:
            print([element.text for element in elements])
            raise Exception

        element.click()

    def expand_see_all_results_search(self, text):
        element = WebDriverWait(self.driver, 10, ignored_exceptions=self.ignored_exceptions).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, self.config.get(self.section, 'see_all_results'))))

        if element.text == 'See all results for \'%s\'' % text:
            element.click()
        else:
            print('wrong text: %s' % element.text)
            raise Exception

    def click_sign_in(self):
        WebDriverWait(self.driver, 10, ignored_exceptions=self.ignored_exceptions).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, self.config.get(self.section, 'sign_in_top_menu')))).click()

    def validate_login_text(self):
        element = None
        for _ in range(10):
            try:
                element = WebDriverWait(self.driver, 10, ignored_exceptions=self.ignored_exceptions).until(EC.element_to_be_clickable((By.CSS_SELECTOR, self.config.get(self.section, 'heather_welcome')))).text
                return element
            except NoSuchElementException:
                time.sleep(0.5)
        else:
            print('heather_welcome text is %s' % element)
            raise Exception
