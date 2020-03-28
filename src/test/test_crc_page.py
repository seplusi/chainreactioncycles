import unittest
from src.main.common.driver import Driver
from src.main.configs.config import Config
from src.main.pageobject.crcHomePage import HomeScreen
from src.main.pageobject.crcAccessoriesPage import AccessoriesScreen
from src.main.pageobject.OneTypeAccessoryScreenPage import OneTypeAccessoryScreen
from src.main.pageobject.crcItemPage import SelectedItemScreen
from src.main.pageobject.searchResultPage import searchResultScreen
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By



class ChainReactionCycles(unittest.TestCase):
    """A sample test class to show how page object works"""

    @classmethod
    def setUpClass(cls):
        cls.driver = Driver('crc_selectors')
        cls.config_obj = Config()
        cls.driver.navigate(cls.config_obj.config.get('URLs', 'crc_base_url'))

    def setUp(self):
        self.driver.navigate(self.config_obj.config.get('URLs', 'crc_base_url'))
        self.homepage = HomeScreen(self.driver, self.config_obj.config)

    @unittest.skip('')
    def test_sunglases(self):
        self.homepage.click_shop_by_category_accessories('accessories')

        self.accessories_page = AccessoriesScreen(self.driver, self.config_obj.config, 'Accessories')
        self.accessories_page.click_item_left_menu('sunglasses')

        self.sunglasses = OneTypeAccessoryScreen(self.driver, self.config_obj.config, 'Accessories > Sunglasses')
        assert self.sunglasses.get_page_heading().text == 'Sunglasses'

        self.sunglasses.click_refinements('In Stock Only')
        self.sunglasses.click_refinements('Sport Sunglasses')
        self.sunglasses.select_discipline('City')
        self.sunglasses.select_rating(4)

        self.sunglasses.select_brand('Tifosi Eyewear')

        assert self.sunglasses.validate_your_choices(['City', 'In Stock Only', 'Tifosi Eyewear', '& Up'])
        assert self.sunglasses.validate_number_items_showing()

        self.sunglasses.sort_price_low_to_high()
        assert self.sunglasses.check_items_are_sorted_by_low_to_high_price()
        assert self.sunglasses.validate_number_items_correct()

#    @unittest.skip('')
    def test_gps(self):
        self.homepage.click_shop_by_category_accessories('nutrition-training')

        self.accessories_page = AccessoriesScreen(self.driver, self.config_obj.config, 'Nutrition & Training')

#        selector = 'div.narrow_status > ul.categories > li.level.level2 > a[href="/<replace>"]'.replace('<replace>', 'gps')
#        elelemtn = WebDriverWait(self.driver.instance, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector))).click()

#        for n in range(10):
#            with open('/var/tmp/page_source.txt', 'w') as f:
#                f.write(self.driver.instance.page_source)

        self.accessories_page.click_item_left_menu('gps')

        self.gps = OneTypeAccessoryScreen(self.driver, self.config_obj.config, 'Nutrition & Training > GPS')
        assert self.gps.get_page_heading().text == 'GPS'

        """
        self.gps.click_refinements('In Stock Only')
        self.gps.select_discipline('City')
        self.gps.select_rating(4)

        self.gps.select_brand('Garmin')

        assert self.gps.validate_your_choices(['City', 'In Stock Only', 'Garmin', '& Up'])
        assert self.gps.validate_number_items_showing()

        self.gps.sort_price_low_to_high()
        assert self.gps.check_items_are_sorted_by_low_to_high_price()
        assert self.gps.validate_number_items_correct()
        """

    @unittest.skip('')
    def test_search_saddles_from_multiple_pages(self):
        self.homepage.type_text_in_search_box('saddles')
        self.homepage.click_category_from_search('saddles')

        self.saddles = OneTypeAccessoryScreen(self.driver, self.config_obj.config, 'Components > Saddles')
        assert self.saddles.get_page_heading().text == 'Saddles'

        self.saddles.click_refinements('In Stock Only')
        self.saddles.select_rating(4)
        self.saddles.click_refinements('Male')

        assert self.saddles.validate_number_items_showing()
        self.saddles.sort_price_low_to_high()
        self.saddles.search_for_item_and_click('PROLOGO T-GALE PAS Tirox Rail Saddle')

        assert SelectedItemScreen(self.driver, self.config_obj.config, 'PROLOGO T-GALE PAS Tirox Rail Saddle').get_item_page_title() == 'PROLOGO T-GALE PAS Tirox Rail Saddle'

    @unittest.skip('')
    def test_search_saddles_from_only_1_page(self):
        self.homepage.type_text_in_search_box('saddles')
        self.homepage.click_category_from_search('saddles')

        self.saddles = OneTypeAccessoryScreen(self.driver, self.config_obj.config, 'Components > Saddles')
        assert self.saddles.get_page_heading().text == 'Saddles'

        self.saddles.click_refinements('In Stock Only')
        self.saddles.select_rating(4)
        self.saddles.click_refinements('Male')
        self.saddles.select_brand('PROLOGO')

        self.saddles.sort_price_low_to_high()
        self.saddles.search_for_item_and_click('PROLOGO T-GALE PAS Tirox Rail Saddle')

        assert SelectedItemScreen(self.driver, self.config_obj.config, 'PROLOGO T-GALE PAS Tirox Rail Saddle').get_item_page_title() == 'PROLOGO T-GALE PAS Tirox Rail Saddle'

    @unittest.skip('')
    def test_selected_item_page(self):
        self.homepage.type_text_in_search_box('PROLOGO T-Gale PAS Tirox Saddle')
        self.homepage.click_specific_item_from_search('PROLOGO T-Gale PAS Tirox Saddle')

        result = searchResultScreen(self.driver, self.config_obj.config, 'Search Results for "prologo t-gale pas tirox saddle"')
        result.click_item('PROLOGO T-Gale PAS Tirox Saddle')

        item = SelectedItemScreen(self.driver, self.config_obj.config, 'PROLOGO T-Gale PAS Tirox Saddle')
        assert item.get_item_page_title() == 'PROLOGO T-Gale PAS Tirox Saddle'

        print('cfvgh')


    def tearDown(self):
        self.take_snapshot_if_failure()
        pass

    @classmethod
    def tearDownClass(cls):
        cls.driver.instance.quit()

    def take_snapshot_if_failure(self):
        for method, error in self._outcome.errors:
            if error:
                with open('/var/tmp/page_source.txt', 'w') as f:
                    f.write(self.driver.instance.page_source)

                self.driver.instance.save_screenshot('/var/tmp/screenshot%s.%d.png' % (self.id(), int(time.time() * 1000)))


if __name__ == "__main__":
    unittest.main()