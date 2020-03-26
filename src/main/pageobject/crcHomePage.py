from src.main.common.HomePage import CommonHomeScreen
from selenium.common.exceptions import StaleElementReferenceException, ElementClickInterceptedException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class HomeScreen(CommonHomeScreen):
    def __init__(self, driver, config):
        super().__init__(driver, config)

    def type_text_in_search_box(self, text):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, 'auto_search'))).send_keys(text)

    def click_category_from_search(self, category):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href^='/%s?']" % category))).click()
