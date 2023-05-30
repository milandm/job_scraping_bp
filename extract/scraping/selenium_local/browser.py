import time

import base64

from bs4 import BeautifulSoup as BS

from extract.scraping.utils import random_wait

from selenium import webdriver

from selenium.webdriver.common.keys import (
    Keys as Selenium_Keys,
)
from selenium.webdriver.common.action_chains import (
    ActionChains,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import (
    expected_conditions as EC,
)
from webdriver_manager.chrome import ChromeDriverManager

PROXY = "socks5://localhost:9050"  # IP:PORT or HOST:PORT


class Browser:
    def __init__(self, wait=None, tor=False, firefox=False, headless=False):
        if wait is None:
            wait = 3
        self.wait = wait
        self.running = False
        self.tor = tor
        self.driver = None
        self.objects = {}
        self.headless = headless
        self.firefox = firefox

    def start(self):
        options = None
        if not self.firefox:
            options = webdriver.ChromeOptions()
        else:
            options = webdriver.FirefoxOptions()

        if self.headless:
            options.add_argument("--headless")

        if self.tor:
            options.add_argument(
                "--proxy-server=%s" % PROXY
            )
            if not self.firefox:
                self.driver = webdriver.Chrome(ChromeDriverManager().install(),
                                               chrome_options=options
                                               )
            else:
                self.driver = webdriver.Firefox(options=options)
        else:
            if not self.firefox:
                self.driver = webdriver.Chrome(ChromeDriverManager().install(),
                                               chrome_options=options
                                               )
            else:
                self.driver = webdriver.Firefox(options=options)
        self.driver.set_page_load_timeout(30)

        self.running = True

    def stop(self):

        self.driver.close()
        self.running = False

    def screenshot(
            self, url, page_height, path=None
    ):

        height = page_height
        options = None
        if not self.firefox:
            options = webdriver.ChromeOptions()
        else:
            options = webdriver.FirefoxOptions()
        options.add_argument("--headless")
        options.add_argument(
            f"--window-size=1920,{height}"
        )
        options.add_argument(
            "--hide-scrollbars"
        )
        temp_driver = None
        if not self.firefox:
            temp_driver = webdriver.Chrome(ChromeDriverManager().install(),
                                           options=options
                                           )
        else:
            temp_driver = webdriver.Firefox(executable_path='./geckodriver',
                                            options=options
                                            )
        temp_driver.get(url)

        url_b64 = base64.urlsafe_b64encode(
            url.encode()
        )
        url_str = "".join(map(chr, url_b64))

        if path is None:
            path = (
                    "data/screenshots/"
                    + url_str
                    + ".png"
            )

        self.random_wait(1)

        temp_driver.save_screenshot(path)
        temp_driver.close()

    def get_html(self):
        html = self.driver.page_source
        return html

    def get(self, url):
        if not self.running:
            self.start()
        self.driver.get(url)

    def keys(self):
        return Selenium_Keys

    def select(self, selector, store=None):

        item = self.driver.find_element_by_css_selector(
            selector
        )

        if store is not None:
            self.objects[store] = item
        return item

    def find_by_xpath(self, xpath, store=None):
        item = self.driver.find_element_by_xpath(
            xpath
        )
        if store is not None:
            self.objects[store] = item
        return item

    def find_elements_by_xpath(self, xpath):
        items = self.driver.find_elements_by_xpath(
            xpath
        )
        return items

    def item(self, selector=None, store=None):
        if selector is not None:
            item = self.select(selector)
        else:
            item = self.objects[store]
        return item

    def click(
            self, item=None, selector=None, store=None
    ):
        if item is None:
            item = self.item(
                selector=selector, store=store
            )
        item.click()

    def type(
            self,
            item=None,
            selector=None,
            store=None,
            keys="",
    ):
        if item is None:
            item = self.item(
                selector=selector, store=store
            )
        item.send_keys(keys)

    def enter(
            self, item=None, selector=None, store=None
    ):
        if item is None:
            item = self.item(
                selector=selector, store=store
            )
        item.send_keys(Selenium_Keys.ENTER)

    def tab(
            self, item=None, selector=None, store=None
    ):
        if item is None:
            item = self.item(
                selector=selector, store=store
            )
        item.send_keys(Selenium_Keys.TAB)

    def delete(
            self, item=None, selector=None, store=None
    ):
        if item is None:
            item = self.item(
                selector=selector, store=store
            )
        item.send_keys(Selenium_Keys.DELETE)

    def submit(
            self, item=None, selector=None, store=None
    ):
        if item is None:
            item = self.item(
                selector=selector, store=store
            )
        item.submit()

    def scroll_to(
            self, item=None, selector=None, store=None
    ):
        if item is None:
            item = self.item(
                selector=selector, store=store
            )
        actions = ActionChains(self.driver)
        actions.move_to_element(item).perform()

    def wait_for(self, selector=None, max=60):
        self.driver.WebDriverWait(
            self.driver, max
        ).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, selector)
            )
        )

    def to_bs(self, html):
        return BS(html, features="lxml")

    def random_wait(self, length):
        wait = random_wait(mean=length)
        time.sleep(wait)

    def get_height(self):
        return self.driver.execute_script(
            "return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight )"
        )

    def grab(
            self,
            url,
            as_soup=True,
            screenshot=False,
            wait=1,
            close=True,
    ):
        if self.running is False:
            self.start()

        result = None

        try:
            self.get(url)

            self.random_wait(wait)

            if screenshot is True:
                page_height = self.get_height()
                self.screenshot(url, page_height)

            html = self.get_html()

            if html is not None:
                if as_soup is True:
                    result = self.to_bs(html)
                else:
                    result = html

        except Exception as e:
            print(f"Browser exception {e}")
            return None

        if close is True:
            self.stop()

        return result

    def login(
            self,
            login_url,
            username_selector,
            password_selector,
            login_btn_selector,
            username,
            password
    ):
        if not self.running:
            self.start()
        try:
            self.get(login_url)
            username_input = self.select(username_selector)
            self.type(item=username_input, keys=username)
            password_input = self.select(selector=password_selector)
            self.type(item=password_input, keys=password)
            login_button = self.select(selector=login_btn_selector)
            self.click(item=login_button)
        except Exception as e:
            print(f'EXCEPTION Browser->login: {e}')

    def scroll_to_end(self):
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while True:

            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # Wait to load the page.
            time.sleep(5)

            # Calculate new scroll height and compare with last scroll height.
            new_height = self.driver.execute_script("return document.body.scrollHeight")

            if new_height == last_height:
                break

            last_height = new_height
