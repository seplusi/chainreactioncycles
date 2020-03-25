from selenium.common.exceptions import StaleElementReferenceException, ElementClickInterceptedException, TimeoutException, ElementNotVisibleException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains


class ItemsScreen(object):
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

    def get_page_heading(self):
        return WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, self.config.get(self.section, 'page_heading'))))

    def click_see_more_brands(self):
        try:
            WebDriverWait(self.driver, 1).until(EC.element_to_be_clickable((By.CSS_SELECTOR, self.config.get(self.section, 'item_see_more')))).click()
        except TimeoutException:
            return

        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, self.config.get(self.section, 'item_see_less'))))

    def click_refinements(self, option_text):
        for _ in range(2):
            try:
                elements = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, self.config.get(self.section, 'all_refine_elements'))))

                for element in elements:
                    if option_text in element.text:
                        break

                element.click()
                break
            except ElementNotVisibleException:
                print('%s not visible' % option_text )
                pass

    def select_rating(self, stars):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.rating-star.rating-%d' % stars))).click()

    def validate_your_choices(self, list_choices):
        for _ in range(2):
            elements = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, self.config.get(self.section, 'your_choices_list'))))
            if len(elements) == len(list_choices):
                break
            print('Searching again for choices')

        values =  [element.text for element in elements]

        for index in range(len(list_choices)):
            if list_choices[index] not in values:
                print(values)

                action = ActionChains(self.driver)
                element = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, self.config.get(self.section, 'item_see_more'))))
                action.move_to_element(element).perform()
                print('Moved to element')

                return False

        if len(list_choices) != len(values):
            return False

        return True

    def validate_number_items_showing(self):
        element = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, self.config.get(self.section, 'nr_items_showing'))))

        element_txt_values = element.text.split(' ')
        if element_txt_values[0] == 'Showing' and element_txt_values[2] == 'items' and element_txt_values[1].isnumeric():
            return True

        return False

    def sort_price_low_to_high(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, self.config.get(self.section, 'best_selling')))).click()

        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, self.config.get(self.section, 'price_low_to_high')))).click()

    def check_items_are_sorted_by_low_to_high_price(self):
        result = False
        elements = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_all_elements_located((By.CLASS_NAME, self.config.get(self.section, 'all_items_price'))))

        values = [element.text.replace('£', '') for element in elements]

        new_lst = []
        for item in values:
            if '-' in item:
                new_lst.append(float(item.split('-')[0]))
            else:
                new_lst.append(float(item))

        if new_lst == sorted(new_lst):
            result = True

        return result

    def validate_number_items_correct(self):
        result = False
        element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, self.config.get(self.section, 'nr_items_showing'))))

        number_items = int(element.text.split(' ')[1])

        if number_items == len(WebDriverWait(self.driver, 10).until(
            EC.visibility_of_all_elements_located((By.CLASS_NAME, self.config.get(self.section, 'all_items_price'))))):
            result = True

        return result

