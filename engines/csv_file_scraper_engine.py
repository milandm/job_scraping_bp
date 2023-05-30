from extract.csv.csv_files_data_extractor import CsvFilesDataExtractor
from log.log_config import get_logger
from extract.scraping.scrape_data.companies_crawler import CompaniesCrawler
from engines.company_internal_profiles_creator.company_internal_profile_creator import CompanyInternalProfilesCreator
from load.store_company_internal_profiles.store_data import StoreData


class CsvFilesScraperEngine:

    def __init__(
            self,
            data_source,
            store_data: StoreData,
            companies_crawler: CompaniesCrawler,
            csv_files_dir,
            delimiter=',',
    ):
        self.logger = get_logger('CsvFilesScraperEngine')
        csv_extract = CsvFilesDataExtractor(
            data_source=data_source,
            files_dir=csv_files_dir,
            delimiter=delimiter
        )
        self.company_internal_profiles_creator = CompanyInternalProfilesCreator(
            data_source, csv_extract
        )
        self.store_data = store_data
        self.companies_crawler = companies_crawler

    def run(self):
        company_internal_profiles = self.company_internal_profiles_creator.get_company_internal_profiles()
        stored_internal_profiles_list = self.store_data.store_profiles(company_internal_profiles)
        self.companies_crawler.set_companies_for_crawling(stored_internal_profiles_list)
        self.companies_crawler.run_crawler()
