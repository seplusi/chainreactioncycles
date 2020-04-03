import unittest
from src.main.common.driver import Driver
from src.main.configs.config import Config
from src.main.pageobject.crcHomePage import HomeScreen
from src.main.pageobject.crcAccessoriesPage import AccessoriesScreen
from src.main.pageobject.OneTypeAccessoryScreenPage import OneTypeAccessoryScreen
from selenium.common.exceptions import TimeoutException
from src.main.pageobject.crcItemPage import SelectedItemScreen
from src.main.pageobject.searchResultPage import searchResultScreen
from src.main.pageobject.crcSingInPage import SignInScreen
import random
import string


class ChainReactionCyclesNegativeCases(unittest.TestCase):
    """A sample test class to show how page object works"""

    @classmethod
    def setUpClass(cls):
        cls.driver = Driver('crc_selectors')
        cls.config_obj = Config()
        cls.driver.navigate(cls.config_obj.config.get('URLs', 'crc_base_url'))

    def setUp(self):
        self.driver.navigate(self.config_obj.config.get('URLs', 'crc_base_url'))
        self.homepage = HomeScreen(self.driver, self.config_obj.config)

#    @unittest.skip('')
    def test_select_non_existant_sunglases_brancd(self):
        self.homepage.click_shop_by_category_accessories('accessories')

        self.accessories_page = AccessoriesScreen(self.driver, self.config_obj.config, 'Accessories', 'Home >')
        self.accessories_page.click_item_left_menu('sunglasses')

        self.sunglasses = OneTypeAccessoryScreen(self.driver, self.config_obj.config, 'Sunglasses', 'Home > Accessories >')
        assert self.sunglasses.get_page_heading().text == 'Sunglasses'

        self.sunglasses.select_stock()
        self.sunglasses.select_discipline('City')
        self.sunglasses.select_rating(4)

        with self.assertRaises(TimeoutException):
            self.sunglasses.select_brand('Ossos')
        assert self.sunglasses.validate_your_choices(['City', 'In Stock Only', '& Up'])

#    @unittest.skip('')
    def test_search_random_string(self):
        product = ''.join(random.choice(string.ascii_lowercase) for i in range(10))
        self.homepage.type_text_in_search_box(product)
        assert self.homepage.get_search_items_list() == ["See all results for '%s'" % product]
        self.homepage.click_see_all_results()

        result = searchResultScreen(self.driver, self.config_obj.config, product, 'Home >', True)
        assert result.check_try_spelling_advice()

#    @unittest.skip('')
    def test_select_from_price_too_high(self):
        self.homepage.type_text_in_search_box('saddles')
        self.homepage.click_category_from_search('saddles')

        saddles = OneTypeAccessoryScreen(self.driver, self.config_obj.config, 'Saddles', 'Home > Components >')
        assert saddles.get_page_heading().text == 'Saddles'

        saddles.select_price_range(min=700)
        assert saddles.validate_your_choices(['Over  £700'])

        assert saddles.get_page_heading().text == 'No items match your search for   “Saddles“'
        assert saddles.get_no_results_message() == 'No products found – please change your price range'

    def tearDown(self):
        self.take_snapshot_if_failure()
        pass

    @classmethod
    def tearDownClass(cls):
        cls.driver.instance.quit()

    def take_snapshot_if_failure(self):
        for method, error in self._outcome.errors:
            if error:
                self.driver.fullpage_screenshot(self.id())
                with open('/var/tmp/page_source.txt', 'w') as f:
                    f.write(self.driver.instance.page_source)


if __name__ == "__main__":
    unittest.main()
