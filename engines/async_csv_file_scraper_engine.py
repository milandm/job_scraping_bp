from engines.company_internal_profiles_creator.async_company_internal_profile_creator import \
    AsyncCompanyInternalProfilesCreator
from extract.csv.csv_files_data_extractor import CsvFilesDataExtractor
from log.log_config import get_logger
from extract.scraping.scrape_data.companies_crawler import CompaniesCrawler
from load.store_company_internal_profiles.async_store_data import AsyncStoreData


class AsyncCsvFilesScraperEngine:

    def __init__(
            self,
            data_source,
            store_data: AsyncStoreData,
            csv_files_dir,
            companies_crawler: CompaniesCrawler,
            delimiter=',',
    ):
        self.logger = get_logger('CsvFilesScraperEngine')
        csv_extract = CsvFilesDataExtractor(
            data_source=data_source,
            files_dir=csv_files_dir,
            delimiter=delimiter
        )
        self.company_internal_profiles_creator = AsyncCompanyInternalProfilesCreator(
            data_source, csv_extract
        )
        self.store_data = store_data
        self.companies_crawler = companies_crawler

    async def run(self):
        company_internal_profiles = await self.company_internal_profiles_creator.get_company_internal_profiles()
        return await self.store_data.store_profiles(company_internal_profiles)

    def run_crawling(self, stored_internal_profiles_list):
        self.companies_crawler.set_companies_for_crawling(stored_internal_profiles_list)
        self.companies_crawler.run_crawler()
