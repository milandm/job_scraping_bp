import scrapy
from bs4 import BeautifulSoup
from scrapy.crawler import CrawlerProcess, CrawlerRunner
from extract.scraping.scrapy.cleaning import soup_to_text
from extract.scraping.scrapy.selenium_request import SeleniumRequest
from extract.scraping.scrapy.items import WebPageItem
from scrapy.linkextractors import LinkExtractor
from scrapy.utils.project import get_project_settings
import os
from twisted.internet import reactor, defer
from log.log_config import get_logger
from scrapy.utils.log import configure_logging
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError
import traceback


os.environ.setdefault('SCRAPY_SETTINGS_MODULE', 'extract.scraping.scrapy.settings')

def run_spider_defered(allowed_domains_list, start_urls_list, scraping_engine_object, my_logger = None):
    if not my_logger:
        my_logger = get_logger('scrapy_spider')
    my_logger.debug(f"run_spider allowed_domains_list len {len(allowed_domains_list)}")
    settings = get_project_settings()
    configure_logging()
    process = CrawlerProcess(settings=settings)
    crawl(process, allowed_domains_list, start_urls_list, scraping_engine_object, my_logger)
    d = process.join()
    d.addCallback(lambda _: scraping_engine_object.on_scrapy_finished())
    d.addErrback(handleFailure)
    reactor.run()


def run_spider_add_new_defered(allowed_domains_list, start_urls_list, scraping_engine_object, my_logger = None):
    my_logger.debug(f"run_spider allowed_domains_list len {len(allowed_domains_list)}")
    settings = get_project_settings()
    configure_logging()
    process = CrawlerProcess(settings=settings)
    crawl(process, allowed_domains_list, start_urls_list, scraping_engine_object, my_logger)
    d = process.join()
    d.addCallback(lambda _: scraping_engine_object.on_scrapy_finished())
    d.addErrback(handleFailure)


@defer.inlineCallbacks
def crawl(runner, allowed_domains_list, start_urls_list, scraping_engine_object, my_logger = None):
    for start_url, allowed_domain in zip(start_urls_list, allowed_domains_list):
        try:
            yield runner.crawl(CustomSiteSpider,
                               allowed_domains=[allowed_domain],
                               start_urls=[start_url],
                               scraping_engine_object=scraping_engine_object)
        except Exception as exception:
            if my_logger:
                my_logger.debug(traceback.format_exc())


def handleFailure(f):
    my_logger = get_logger("handleFailure")
    my_logger.debug(str(f.getTraceback()))
    f.trap(RuntimeError)


def run_spider(allowed_domains_list, start_urls_list, scraping_engine_object, my_logger = None):
    my_logger.debug(f"run_spider allowed_domains_list len {len(allowed_domains_list)}")
    settings = get_project_settings()
    configure_logging()
    process = CrawlerProcess(settings=settings)
    for start_url, allowed_domain in zip(start_urls_list, allowed_domains_list):
        try:
            process.crawl(CustomSiteSpider,
                          allowed_domains=[allowed_domain],
                          start_urls=[start_url],
                          scraping_engine_object=scraping_engine_object)
        except Exception as exception:
            if my_logger:
                my_logger.debug(exception)
    try:
        d = process.join()
        d.addBoth(lambda _: scraping_engine_object.on_scrapy_finished())
    except Exception as exception:
        if my_logger:
            my_logger.debug(exception)
    reactor.run()


def run_spider_add_new(allowed_domains_list, start_urls_list, scraping_engine_object, my_logger = None):
    my_logger.debug(f"run_spider allowed_domains_list len {len(allowed_domains_list)}")
    settings = get_project_settings()
    configure_logging()
    process = CrawlerProcess(settings=settings)
    for start_url, allowed_domain in zip(start_urls_list, allowed_domains_list):
        try:
            process.crawl(CustomSiteSpider,
                          allowed_domains=[allowed_domain],
                          start_urls=[start_url],
                          scraping_engine_object=scraping_engine_object)
        except Exception as exception:
            if my_logger:
                my_logger.debug(exception)
    try:
        d = process.join()
    except Exception as exception:
        if my_logger:
            my_logger.debug(exception)


def stop_reactor():
    reactor.stop()


class SpiderRunner:

    def __init__(self, scraping_engine_object):
        self.scraping_engine_object = scraping_engine_object

        self.settings = get_project_settings()
        configure_logging()

    def run_spider(self, allowed_domains_list, start_urls_list):
        process = CrawlerRunner(settings=self.settings)
        for start_url, allowed_domain in zip(start_urls_list, allowed_domains_list):
            try:
                process.crawl(CustomSiteSpider, allowed_domains=[allowed_domain],
                              start_urls=[start_url],
                              scraping_engine_object=self.scraping_engine_object)
            except Exception as exception:
                self.my_logger.debug(exception)

        try:
            d = process.join()
            d.addBoth(lambda _: self.scraping_engine_object.on_scrapy_finished())
        except Exception as exception:
            self.my_logger.debug(exception)
        # d.addBoth(lambda _: reactor.stop())
        reactor.run()

    def run_itteration(self):
        process = CrawlerRunner(settings=self.settings)
        # process = CrawlerProcess(settings=settings)
        # logger.debug('########### urls and allowed domains ###############')
        for start_url, allowed_domain in zip(self.start_urls_list, self.allowed_domains_list):
            # logger.debug(f"run_spider -> start_url, allowed_domain: {start_url} {allowed_domain}")
            process.crawl(CustomSiteSpider, allowed_domains=[allowed_domain],
                          start_urls=[start_url],
                          scraping_engine_object=self.scraping_engine_object)
        d = process.join()
        d.addBoth(lambda _: reactor.stop())
        # d.addBoth(lambda _: reactor.stop())
        reactor.run()

class CustomSiteSpider(scrapy.Spider):
    name = 'customsite'
    # custom_settings = {
    #     # 'CONCURRENT_REQUESTS': 10,
    #     'CONCURRENT_REQUESTS_PER_DOMAIN': 10,
    #     'DOWNLOAD_DELAY': 4.5
    # }

    LINKS_LIMIT = 20

    def __init__(self, **kwargs):
        # super(CustomSiteSpider, self).__init__(**kwargs)
        self.my_logger = get_logger("CustomSiteSpider")
        super().__init__(**kwargs)
        self.my_logger.debug(" __init__ CustomSiteSpider ")
        self.scraping_engine_object = kwargs.get('scraping_engine_object')

        # self.allowed_domains = []
        self.allowed_domains = list()
        for domain in kwargs.get('allowed_domains'):
            self.allowed_domains.append(domain)
        # self.start_urls = []
        self.start_urls = list()
        for url in kwargs.get('start_urls'):
            self.start_urls.append(url)

    def start_requests(self):
        # self.start_urls.append(self.start_urls[-1])
        self.logger.debug('start_requests')
        for url in self.start_urls:
            try:
                yield SeleniumRequest(url=url,
                                      callback=self.parse,
                                      errback=self.errback_httpbin,
                                      headers={('User-Agent', 'Mozilla/5.0')})
            except Exception as exception:
                self.my_logger.debug(exception)

            # yield SeleniumRequest(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        # item = self.get_page_item(response)
        # # self.my_logger.debug(f'response: {response}')
        # yield item


        try:
            link_extractor = LinkExtractor(allow_domains=self.allowed_domains)
        except Exception as exception:
            self.my_logger.debug(exception)
        links = link_extractor.extract_links(response)
        if len(links) > CustomSiteSpider.LINKS_LIMIT:
            links  = links[:CustomSiteSpider.LINKS_LIMIT]
        for link in links:
            try:
                yield SeleniumRequest(url=link.url,
                                      callback=self.parse_items,
                                      # ,
                                      # script='window.scrollTo(0, document.body.scrollHeight);'
                                      dont_filter=True,
                                      errback=self.errback_httpbin,
                                      headers={('User-Agent', 'Mozilla/5.0')})
            except Exception as exception:
                self.my_logger.debug(exception)
            # yield SeleniumRequest(url=link.url, callback=self.parse_items, dont_filter=True)

    def parse_items(self, response):
        item = self.get_page_item(response)
        # self.my_logger.debug(f'parse_items -> item page_url: {item["page_url"]}')
        yield item

    def get_page_item(self, response):
        response_body = response.body.decode(encoding="UTF-8")
        # soup = BeautifulSoup(response_body, "html5lib")
        soup = BeautifulSoup(response_body, 'lxml')
        # soup = BeautifulSoup(response_body, features="html.parser")

        text = soup_to_text(soup)
        url = response.url
        item = WebPageItem()
        item['page_url'] = url
        item['company_domain'] = self.allowed_domains[0]
        item['page_content'] = text
        # item['error'] = response.
        # self.my_logger.debug(f'get_page_item -> item created page_url: {url}')
        return item

    def errback_httpbin(self, failure):
        # log all errback failures,
        # in case you want to do something special for some errors,
        # you may need the failure's type
        self.my_logger.debug(repr(failure))

        # if isinstance(failure.value, HttpError):
        if failure.check(HttpError):
            # you can get the response
            response = failure.value.response
            self.my_logger.debug('HttpError on %s', response.url)

        # elif isinstance(failure.value, DNSLookupError):
        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            self.my_logger.debug('DNSLookupError on %s', request.url)

        # elif isinstance(failure.value, TimeoutError):
        elif failure.check(TimeoutError):
            request = failure.request
            self.my_logger.debug('TimeoutError on %s', request.url)