from typing import List
from load.models.company_internal_item import CompanyInternalItem
from load.models.company_internal_profile import CompanyInternalProfile
from log.log_config import get_logger
from load.s3.s3_api import S3Api
from extract.scraping.scrapy.spiders.custom_site_spider import run_spider_defered, stop_reactor
from utils.utils import make_list_unique


class CompaniesCrawler:

    def __init__(
            self,
            data_source: str,
            s3: S3Api,
            db
    ):
        self.logger = get_logger('CompaniesCrawler')
        self.data_source = data_source
        self.s3 = s3
        self.db = db
        self.companies_for_crawling = {}
        self.crawled_domains = set()

    def set_companies_for_crawling(self, company_internal_profiles_list: List[CompanyInternalProfile]):
        self.companies_for_crawling = {
            company.base_web_address: company.full_web_address for company in company_internal_profiles_list
        }

    def run_crawler(self):
        companies_domain_list = self.companies_for_crawling.keys()
        companies_website_list = self.companies_for_crawling.values()
        run_spider_defered(
            allowed_domains_list=companies_domain_list,
            start_urls_list=companies_website_list,
            scraping_engine_object=self
        )

    def store_scraped_content_callback(self, item):
        self.logger.debug('############## CALLBACK ##############')
        try:
            page_url = item['page_url']
            company_domain = item["company_domain"]
            data = item['page_content']
            self.logger.debug(f'page_url: {item["page_url"]}, company_domain: {item["company_domain"]}')
            success = self.s3.put(key=page_url, data=data)
            if success:
                self.logger.debug('s3_bucket put done')
                self.store_company_internal_item_to_profile(
                    page_url=page_url,
                    company_domain=company_domain
                )
                self.crawled_domains.add(company_domain)
                self.logger.debug('store_internal_item_to_profile done')
            else:
                self.logger.debug("Couldn't store scraped data to s3")
        except Exception as e:
            self.logger.debug("add_company_internal_item_to_profile " + str(e))
        self.logger.debug('############## CALLBACK END ##############')

    def on_scrapy_finished(self):
        stop_reactor()
        if self.companies_for_crawling:
            self.run_crawler()
        self.logger.debug('########## scrapy crawler finished ##########')
        self.logger.debug(f'number of crawled companies: {len(self.crawled_domains)}, '
                          f'out of {len(self.companies_for_crawling)}')

    def store_company_internal_item_to_profile(self, page_url, company_domain):
        try:
            company_internal_item = CompanyInternalItem(
                full_web_address=page_url,
                base_web_address=company_domain,
                bucket_name=self.s3.bucket_name,
                bucket_path_list=[page_url],
                language=''
            )
            company_profile = self.db.query_company_profile_by_base_web_address(
                company_domain
            )
            self.logger.debug(f'{company_profile}')
            if company_profile:
                company_internal_profile = CompanyInternalProfile.from_dict(company_profile)
                company_internal_profile.company_internal_items.append(company_internal_item)

                get_list_unique_key_method = lambda internal_item: company_internal_item.bucket_path_list[0]
                company_internal_items_unique = make_list_unique(company_internal_profile.company_internal_items,
                                                                 get_list_unique_key_method)
                company_internal_profile.company_internal_items = company_internal_items_unique
                self.db.store_company_internal_profile_data(company_internal_profile)
        except Exception as e:
            self.logger.debug(f'Exception occurred in store_company_internal_item_to_profile {e}')
