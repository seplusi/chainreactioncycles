from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException, ElementClickInterceptedException
from PIL import Image
import os
import time


class Driver:

    def __init__(self, section):
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-popup-blocking");
        options.add_experimental_option('w3c', False)
        options.add_argument("--user-data-dir=/home/luis/Programs/crc_profile")

        self.instance = webdriver.Chrome(executable_path="/home/luis/Programs/chromedriver", options=options, service_args=["--error", "--log-path=/var/tmp/selenium.log"])
        self.section = section
        self.ignored_exceptions = (StaleElementReferenceException, ElementClickInterceptedException,)

    def navigate(self, url):
        if isinstance(url, str):
            self.instance.get(url)
        else:
            raise TypeError("URL must be a string.")

    def move_to_element(self, selector):
        # Move to discipline selection
        action = ActionChains(self.instance)
        element = WebDriverWait(self.instance, 10, ignored_exceptions=self.ignored_exceptions).until(EC.visibility_of_element_located((By.CSS_SELECTOR, selector)))
        action.move_to_element(element).perform()

    def fullpage_screenshot(self, id):
        print("Starting chrome full page screenshot workaround ...")

        total_width = self.instance.execute_script("return document.body.offsetWidth")
        total_height = self.instance.execute_script("return document.body.parentNode.scrollHeight")
        viewport_width = self.instance.execute_script("return document.body.clientWidth")
        viewport_height = self.instance.execute_script("return window.innerHeight")
#        print("Total: ({0}, {1}), Viewport: ({2},{3})".format(total_width, total_height,viewport_width,viewport_height))
        rectangles = []

        i = 0
        while i < total_height:
            ii = 0
            top_height = i + viewport_height

            if top_height > total_height:
                top_height = total_height

            while ii < total_width:
                top_width = ii + viewport_width

                if top_width > total_width:
                    top_width = total_width

#                print("Appending rectangle ({0},{1},{2},{3})".format(ii, i, top_width, top_height))
                rectangles.append((ii, i, top_width,top_height))

                ii = ii + viewport_width

            i = i + viewport_height

        stitched_image = Image.new('RGB', (total_width, total_height))
        previous = None
        part = 0

        for rectangle in rectangles:
            if not previous is None:
                self.instance.execute_script("window.scrollTo({0}, {1})".format(rectangle[0], rectangle[1]))
#                print("Scrolled To ({0},{1})".format(rectangle[0], rectangle[1]))

            file_name = "part_{0}.png".format(part)
#            print("Capturing {0} ...".format(file_name))

            self.instance.get_screenshot_as_file(file_name)
            screenshot = Image.open(file_name)

            if rectangle[1] + viewport_height > total_height:
                offset = (rectangle[0], total_height - viewport_height)
            else:
                offset = (rectangle[0], rectangle[1])

#            print("Adding to stitched image with offset ({0}, {1})".format(offset[0],offset[1]))
            stitched_image.paste(screenshot, offset)

            del screenshot
            os.remove(file_name)
            part = part + 1
            previous = rectangle

        stitched_image.save('/var/tmp/screenshot%s.%d.png' % (id, int(time.time() * 1000)))
        print("Finishing chrome full page screenshot workaround...")
        return True
