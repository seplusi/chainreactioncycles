from selenium.common.exceptions import StaleElementReferenceException, ElementClickInterceptedException, TimeoutException, ElementNotVisibleException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains


class OneTypeAccessoryScreen(object):
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
            print(' '.join([element.text for element in elements]))
            raise Exception

    def get_page_heading(self):
        return WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, self.config.get(self.section, 'page_heading'))))

    def _click_see_more_brands(self):
        try:
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, self.config.get(self.section, 'item_see_more')))).click()
        except TimeoutException:
            return

        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, self.config.get(self.section, 'item_see_less'))))

    def select_brand(self, item_brand):
        # Expand more if it exists
        self._click_see_more_brands()

        # Select brand
        selector = self.config.get(self.section, 'select_brand').replace('<replace>', item_brand)
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector))).click()

        # Move to discipline selection
        action = ActionChains(self.driver)
        element = WebDriverWait(self.driver, 10, ignored_exceptions=self.ignored_exceptions).until(EC.visibility_of_element_located((By.CSS_SELECTOR, selector)))
        action.move_to_element(element).perform()

        # Verify that discipline is selected
        selector = self.config.get(self.section, 'clicked_select_brand').replace('<replace>', item_brand)
        WebDriverWait(self.driver, 10, ignored_exceptions=self.ignored_exceptions).until(EC.visibility_of_element_located((By.CSS_SELECTOR, selector)))

    def click_refinements(self, option_text):
        for _ in range(2):
            try:
                elements = WebDriverWait(self.driver, 10, ignored_exceptions=self.ignored_exceptions).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, self.config.get(self.section, 'all_refine_elements'))))

                for element in elements:
                    if option_text in element.text:
                        break

                element.click()
                break
            except ElementNotVisibleException:
                print('%s not visible' % option_text )
                pass

    def select_discipline(self, option_text):
        # Click discipline
        selector = self.config.get(self.section, 'select_discipline').replace('<replace>', option_text)
        print(selector)
        WebDriverWait(self.driver, 10, ignored_exceptions=self.ignored_exceptions).until(EC.visibility_of_element_located((By.CSS_SELECTOR, selector)))
        WebDriverWait(self.driver, 10, ignored_exceptions=self.ignored_exceptions).until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector))).click()

        # Move to discipline selection
        action = ActionChains(self.driver)
        element = WebDriverWait(self.driver, 10, ignored_exceptions=self.ignored_exceptions).until(EC.visibility_of_element_located((By.CSS_SELECTOR, selector)))
        action.move_to_element(element).perform()

        # Verify that discipline is selected
        selector = self.config.get(self.section, 'clicked_select_discipline').replace('<replace>', option_text)
        WebDriverWait(self.driver, 10, ignored_exceptions=self.ignored_exceptions).until(EC.visibility_of_element_located((By.CSS_SELECTOR, selector)))

    def select_rating(self, stars):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.rating-star.rating-%d' % stars))).click()

    def validate_your_choices(self, list_choices):
        # Validate the refinement choices
        for _ in range(2):
            elements = WebDriverWait(self.driver, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, self.config.get(self.section, 'your_choices_list'))))
            if len(elements) == len(list_choices):
                break
            print('Searching again for choices. Got %s and should have %s' % (str([element.text for element in elements]), str(list_choices)))
        else:
            raise Exception

        values = [element.text for element in elements]

        for index in range(len(list_choices)):
            if list_choices[index] not in values:
                print(values)
                return False

        if len(list_choices) != len(values):
            print('%s != %s' % (str(list_choices), str([element.text for element in elements])))
            return False

        return True

    def validate_number_items_showing(self):
        # Validate the string of how many items are being shown.
        element = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, self.config.get(self.section, 'nr_items_showing'))))

        element_txt_values = element.text.split(' ')
        if len(element_txt_values) == 6:
            results_lst = ['Showing', True, '-', True, 'of', True]
        else:
            results_lst = ['Showing', True, 'items']

        list_result = []
        for item in element_txt_values:
            if item.isnumeric():
                list_result.append(True)
            else:
                list_result.append(item)

        return list_result == results_lst

    def sort_price_low_to_high(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, self.config.get(self.section, 'best_selling')))).click()

        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, self.config.get(self.section, 'price_low_to_high')))).click()

    def check_items_are_sorted_by_low_to_high_price(self):
        # Get all items prices and validate they are sorted by price
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

        # Get the number of items in "Showing NR items"
        element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, self.config.get(self.section, 'nr_items_showing'))))

        if 'of' in element.text:
            number_items = int(element.text.split(' ')[-1])
        else:
            number_items = int(element.text.split(' ')[1])

        # Some items appear but without a price and "Currently Unavailable" instead. Get these ones
        nr_unavailable_prices = 0
        try:
            bundle_mgss =  WebDriverWait(self.driver, 10).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, 'bundle_msg')))
            if bundle_mgss:
                for msg in bundle_mgss:
                    if msg.text == 'Currently Unavailable':
                        nr_unavailable_prices = nr_unavailable_prices + 1
        except TimeoutException:
            pass

        # Verify the numbers match
        all_items = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_all_elements_located((By.CLASS_NAME, self.config.get(self.section, 'all_items_price'))))
        if number_items == len(all_items) + nr_unavailable_prices:
            result = True
        else:
            print([element.text.replace('£', '') for element in all_items])
            print('Expected number of items=%d. Real number of elements=%d' % (number_items, len(all_items)))

        return result

    def total_number_items(self):
        # Get the number of items in "Showing NR items" or "Showing 1 - 48 of NR"
        element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, self.config.get(self.section, 'nr_items_showing'))))

        if 'of' in element.text:
            number_items = int(element.text.split(' ')[-1])
        else:
            number_items = int(element.text.split(' ')[1])

        return number_items

    def get_nr_items_per_page(self):
        # Get active number items per page. Top right hand corner
        value = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, self.config.get(self.section, 'active_nr_items_per_page')))).text

        return int(value)

    def get_pagination_elements(self, nr_items_p_page):
        nr_selected_items = self.total_number_items()

        if nr_items_p_page > nr_selected_items:
            return False

        return WebDriverWait(self.driver, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div.pagination > a')))

    def search_for_item_and_click(self, item_name):
        # Get number items per page
        nr_items_p_page = self.get_nr_items_per_page()

        # Get number of pages from bottom right hand corner
        nr_pages = self.get_pagination_elements(nr_items_p_page)

        if nr_pages:
            # If multiple pages exist then go thought them
            for page_nr in range(len(nr_pages) - 1):
                for num in range(3):
                    all_items = WebDriverWait(self.driver, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, self.config.get(self.section, 'search_all_items'))))
                    if len(all_items) == nr_items_p_page:
                        break
                    else:
                        print('Only got %s items instead %d' % (len(all_items), nr_items_p_page))
                else:
                    print('Could not find %d items' % nr_items_p_page)

                if item_name.lower() in [item.text.lower() for item in all_items]:
                    break
                else:
                    self.get_pagination_elements(nr_items_p_page)[page_nr + 1].click()

        selector = self.config.get(self.section, 'search_item_with_name').replace('<replace>', 'Components-Saddles-%s' % item_name)
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector))).click()
