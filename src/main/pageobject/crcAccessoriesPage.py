from selenium.common.exceptions import StaleElementReferenceException, ElementClickInterceptedException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time


class AccessoriesScreen():
    def __init__(self, driver, config, title):
        self.driver = driver.instance
        self.config = config
        self.section = driver.section
        self.ignored_exceptions = (StaleElementReferenceException, ElementClickInterceptedException,)
        self._wait_for_loading_page()
        self._validate_breadcrumb(title)

    def _wait_for_loading_page(self):
        WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'ul.brands-list')))

    def _validate_breadcrumb(self, title):
        elements = WebDriverWait(self.driver, 10).until(EC.visibility_of_all_elements_located(
            (By.CSS_SELECTOR, self.config.get(self.section, 'accessories_breadcrumb'))))

        if not ' '.join([element.text for element in elements]) == 'Home > %s' % title:
            raise Exception

    def click_item_left_menu(self, item_name):
        action = ActionChains(self.driver)
        action.send_keys(Keys.PAGE_DOWN).perform()

        for _ in range(2):
            selector = self.config.get(self.section, 'item_left_menu').replace('<replace>', item_name)
            try:
                time.sleep(1)
                elelemtn = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
                self.driver.execute_script("arguments[0].setAttribute('style', arguments[1]);", elelemtn, "background: yellow; border: 2px solid red;")

                elelemtn.click()
                break
            except ElementClickInterceptedException:
                time.sleep(1)
                print('Other element other than GPS would be clicked. Going to try again')
                pass
        else:
            raise Exception


