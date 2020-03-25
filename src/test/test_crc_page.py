import unittest
from src.main.common.driver import Driver
from src.main.configs.config import Config
from src.main.pageobject.crcHomePage import HomeScreen
from src.main.pageobject.crcAccessoriesPage import AccessoriesScreen
from src.main.pageobject.crcItemPage import ItemsScreen

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

#    @unittest.skip('')
    def test_sunglases(self):
        self.homepage.click_shop_by_category()
        self.driver.navigate(self.config_obj.config.get('URLs', 'crc_base_url'))
        self.homepage.click_shop_by_category_accessories('accessories')

        self.accessories_page = AccessoriesScreen(self.driver, self.config_obj.config, 'Accessories')
        self.accessories_page.click_item_left_menu('sunglasses')

        self.sunglasses = ItemsScreen(self.driver, self.config_obj.config, 'Accessories > Sunglasses')
        assert self.sunglasses.get_page_heading().text == 'Sunglasses'

        self.sunglasses.click_refinements('In Stock Only')
        self.sunglasses.click_refinements('Sport Sunglasses')
        self.sunglasses.click_refinements('City')
        self.sunglasses.select_rating(4)

        self.sunglasses.click_see_more_brands()
        self.sunglasses.click_refinements('Tifosi Eyewear')

        assert self.sunglasses.validate_your_choices(['City', 'In Stock Only', 'Tifosi Eyewear', '& Up'])
        assert self.sunglasses.validate_number_items_showing()

        self.sunglasses.sort_price_low_to_high()
        assert self.sunglasses.check_items_are_sorted_by_low_to_high_price()
        assert self.sunglasses.validate_number_items_correct()

    @unittest.skip('')
    def test_gps(self):
        self.homepage.click_shop_by_category()
        self.homepage.click_shop_by_category_accessories('nutrition-training')

        self.accessories_page = AccessoriesScreen(self.driver, self.config_obj.config, 'Nutrition & Training')
        self.accessories_page.click_item_left_menu('gps')

        self.gps = ItemsScreen(self.driver, self.config_obj.config, 'Nutrition & Training > GPS')
        assert self.gps.get_page_heading().text == 'GPS'

        self.gps.click_refinements('In Stock Only')
        self.gps.click_refinements('City')
        self.gps.select_rating(4)

        self.gps.click_see_more_brands()
        self.gps.click_refinements('Garmin')

        assert self.gps.validate_your_choices(['City', 'In Stock Only', 'Garmin', '& Up'])
        assert self.gps.validate_number_items_showing()

        self.gps.sort_price_low_to_high()
        assert self.gps.check_items_are_sorted_by_low_to_high_price()
        assert self.gps.validate_number_items_correct()

    def tearDown(self):
        self.take_snapshot_if_failure()
        pass

    @classmethod
    def tearDownClass(cls):
        cls.driver.instance.quit()

    def take_snapshot_if_failure(self):
        for method, error in self._outcome.errors:
            if error:
                self.driver.instance.save_screenshot('/var/tmp/screenshot%s.png' % self.id())


if __name__ == "__main__":
    unittest.main()