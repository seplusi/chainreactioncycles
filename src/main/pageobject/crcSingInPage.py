from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException, ElementClickInterceptedException


class SignInScreen(object):
    def __init__(self, driver, config, title, breadcrumb_path):
        self.driver = driver.instance
        self.config = config
        self.section = driver.section
        self.ignored_exceptions = (StaleElementReferenceException, ElementClickInterceptedException,)
        self.breadcrumb_path = breadcrumb_path
        self.title = title
        self._validate_breadcrumb()
        self._validate_login_subheads()

    def _validate_breadcrumb(self):
        elements = WebDriverWait(self.driver, 10).until(EC.visibility_of_all_elements_located(
            (By.CSS_SELECTOR, self.config.get(self.section, 'accessories_breadcrumb'))))

        if not ' '.join([element.text for element in elements]) == '%s %s' % (self.breadcrumb_path, self.title):
            raise Exception

    def _validate_login_subheads(self):
        elements = WebDriverWait(self.driver, 10).until(EC.visibility_of_all_elements_located(
            (By.CSS_SELECTOR, self.config.get(self.section, 'sign_in_subheads'))))

        if not sorted([element.text for element in elements]) == ['New Customers', 'Returning Customers']:
            print('Got %s instead of %s' % (sorted([element.text for element in elements]),
                                            ['New Customers', 'Returning Customers']))
            raise Exception

    def perform_login(self, username, password):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, self.config.get(self.section, 'username')))).send_keys(username)
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, self.config.get(self.section, 'password')))).send_keys(password)

        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, self.config.get(self.section, 'sign_in_button')))).click()
