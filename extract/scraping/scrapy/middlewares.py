# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from importlib import import_module
# useful for handling different item types with a single interface
from scrapy.exceptions import NotConfigured
from scrapy.http import HtmlResponse
from selenium.webdriver.support.wait import WebDriverWait
import time
from extract.scraping.scrapy.selenium_request import SeleniumRequest
from log.log_config import get_logger
import traceback
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


class CustomSiteCrawlerSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    def __init__(self, driver_name, driver_executable_path, driver_arguments,
                 browser_executable_path):
        self.my_logger = get_logger("CustomSiteCrawlerSpiderMiddleware")

        webdriver_base_path = f'selenium.webdriver.{driver_name}'

        driver_class_module = import_module(f'{webdriver_base_path}.webdriver')
        driver_class = getattr(driver_class_module, 'WebDriver')

        driver_options_module = import_module(f'{webdriver_base_path}.options')
        driver_options_class = getattr(driver_options_module, 'Options')

        driver_options = driver_options_class()
        if browser_executable_path:
            driver_options.binary_location = browser_executable_path
        for argument in driver_arguments:
            driver_options.add_argument(argument)


        # profile = driver_options.profile
        profile = webdriver.FirefoxProfile()
        profile.set_preference('javascript.enabled', True)
        profile.update_preferences()
        # browser = webdriver.Firefox(firefox_profile=profile)

        try:
            driver_options.profile = profile
        except Exception as error:
            self.my_logger.debug(error)

        # driver_options.profile(profile)

        # driver_options.headless = False

        driver_kwargs = {
            'executable_path': driver_executable_path,
            f'{driver_name}_options': driver_options
        }

        # 'driver_name', 'driver_executable_path', 'driver_arguments', and 'browser_executable_path'

        self.driver = driver_class(**driver_kwargs)

        # firefox_profile = self.driver.firefox_profile
        # if firefox_profile:
        #     firefox_profile = webdriver.FirefoxProfile()
        #     firefox_profile.set_preference('javascript.enabled', True)
        #     firefox_profile.update_preferences()

        # options = webdriver.ChromeOptions()
        # options.add_argument("--headless")
        # self.driver = webdriver.Chrome(ChromeDriverManager().install(),
        #                                chrome_options=options
        #                                )

    # @classmethod
    # def from_crawler(cls, crawler):
    #     return cls(crawler.settings)

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        # s = cls()

        # This method is used by Scrapy to create your spiders.
        driver_name = crawler.settings.get('SELENIUM_DRIVER_NAME')
        driver_executable_path = crawler.settings.get('SELENIUM_DRIVER_EXECUTABLE_PATH')
        browser_executable_path = crawler.settings.get('SELENIUM_BROWSER_EXECUTABLE_PATH')
        driver_arguments = crawler.settings.get('SELENIUM_DRIVER_ARGUMENTS')


        # profile = webdriver.FirefoxProfile()
        # profile.set_preference("general.useragent.override",
        #                        "Mozilla/5.0 (X11; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0")
        # profile.set_preference("javascript.enabled", True)
        # # broswer = webdriver.Firefox(profile)



        if not driver_name or not driver_executable_path:
            raise NotConfigured(
                'SELENIUM_DRIVER_NAME and SELENIUM_DRIVER_EXECUTABLE_PATH must be set'
            )

        middleware = cls(
            driver_name=driver_name,
            driver_executable_path=driver_executable_path,
            driver_arguments=driver_arguments,
            browser_executable_path=browser_executable_path
        )

        # middleware.driver.firefox_profile = profile

        crawler.signals.connect(middleware.spider_closed, signals.spider_closed)
        # return middleware

        # middleware = cls(crawler.settings)
        crawler.signals.connect(middleware.spider_opened, signal=signals.spider_opened)

        return middleware

        # return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.
        self.my_logger.debug("process_spider_input " + str(response))
        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        self.my_logger.debug('[process_spider_exception] Exception caught: %s' % str(exception))

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

    def process_request(self, request, spider):
        if not isinstance(request, SeleniumRequest):
            return None

        cookies = {
            'sucuri_cloudproxy_uuid_3763320b2': 'b0cda35ef63b5b3df4215f2b7902756f',
        }

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0',
            'TE': 'Trailers',
        }

        request.cookies = cookies
        request.headers = headers

        try:
            self.driver.get(request.url)

            # self.driver.get(request.url)
            self.scroll_to_end()
            for cookie_name, cookie_value in request.cookies.items():
                self.driver.add_cookie(
                    {
                        'name': cookie_name,
                        'value': cookie_value
                    }
                )

            if request.wait_until:
                WebDriverWait(self.driver, request.wait_time).until(
                    request.wait_until
                )

            if request.screenshot:
                request.meta['screenshot'] = self.driver.get_screenshot_as_png()

            if request.script:
                self.driver.execute_script(request.script)

            body = str.encode(self.driver.page_source)

            # Expose the driver via the "meta" attribute
            request.meta.update({'driver': self.driver})

            return HtmlResponse(
                self.driver.current_url,
                body=body,
                encoding='utf-8',
                request=request
            )

        except Exception as e:
            self.my_logger.debug(f'driver.get: {e}')

        return None

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

    def spider_closed(self):
        try:
            self.driver.quit()
        except Exception as e:
            self.my_logger.debug("spider_closed " + str(e))

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        # pass
        self.my_logger.debug(str(exception))
    #     "error process_exception "


class TechcrunchListDownloaderMiddleware:

    def __init__(self, driver_name, driver_executable_path, driver_arguments,
                 browser_executable_path):
        self.my_logger = get_logger("TechcrunchListDownloaderMiddleware")

        webdriver_base_path = f'selenium.webdriver.{driver_name}'

        driver_class_module = import_module(f'{webdriver_base_path}.webdriver')
        driver_class = getattr(driver_class_module, 'WebDriver')

        driver_options_module = import_module(f'{webdriver_base_path}.options')
        driver_options_class = getattr(driver_options_module, 'Options')

        driver_options = driver_options_class()
        if browser_executable_path:
            driver_options.binary_location = browser_executable_path
        for argument in driver_arguments:
            driver_options.add_argument(argument)

        driver_kwargs = {
            'executable_path': driver_executable_path,
            f'{driver_name}_options': driver_options
        }

        self.driver = driver_class(**driver_kwargs)

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        driver_name = crawler.settings.get('SELENIUM_DRIVER_NAME')
        driver_executable_path = crawler.settings.get('SELENIUM_DRIVER_EXECUTABLE_PATH')
        browser_executable_path = crawler.settings.get('SELENIUM_BROWSER_EXECUTABLE_PATH')
        driver_arguments = crawler.settings.get('SELENIUM_DRIVER_ARGUMENTS')

        if not driver_name or not driver_executable_path:
            raise NotConfigured(
                'SELENIUM_DRIVER_NAME and SELENIUM_DRIVER_EXECUTABLE_PATH must be set'
            )

        middleware = cls(
            driver_name=driver_name,
            driver_executable_path=driver_executable_path,
            driver_arguments=driver_arguments,
            browser_executable_path=browser_executable_path
        )

        crawler.signals.connect(middleware.spider_closed, signals.spider_closed)

        return middleware

    def process_request(self, request, spider):
        if not isinstance(request, SeleniumRequest):
            return None

        try:
            self.driver.get(request.url)

            # self.driver.get(request.url)
            self.scroll_to_end()
            for cookie_name, cookie_value in request.cookies.items():
                self.driver.add_cookie(
                    {
                        'name': cookie_name,
                        'value': cookie_value
                    }
                )

            if request.wait_until:
                WebDriverWait(self.driver, request.wait_time).until(
                    request.wait_until
                )

            if request.screenshot:
                request.meta['screenshot'] = self.driver.get_screenshot_as_png()

            if request.script:
                self.driver.execute_script(request.script)

            body = str.encode(self.driver.page_source)

            # Expose the driver via the "meta" attribute
            request.meta.update({'driver': self.driver})

            return HtmlResponse(
                self.driver.current_url,
                body=body,
                encoding='utf-8',
                request=request
            )

        except Exception as e:
            self.my_logger.debug(f'driver.get: {e}')

        return None



    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        # pass
        self.my_logger.debug(str(exception))
    #     "error process_exception "

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

    def spider_closed(self):
        try:
            self.driver.quit()
        except Exception as e:
            self.my_logger.debug("spider_closed " + str(e))

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

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        self.my_logger.debug('[process_spider_exception] Exception caught: %s' % str(exception))
