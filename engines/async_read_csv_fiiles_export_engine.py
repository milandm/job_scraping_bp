from extract.csv.csv_files_data_extractor import CsvFilesDataExtractor
from load.models.company_internal_profile import CompanyInternalProfile
from load.mongodb.mongodb_async import MongoDBAsync
from log.log_config import get_logger
from export.export_data.async_company_profiles_export import AsyncCompanyProfilesExport
from engines.company_internal_profiles_creator.async_company_internal_profile_creator import AsyncCompanyInternalProfilesCreator


class AsyncReadCsvFilesExportEngine:

    def __init__(
            self,
            data_source,
            db: MongoDBAsync,
            csv_files_dir,
            company_profiles_export: AsyncCompanyProfilesExport,
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
        self.db = db
        self.company_profiles_export = company_profiles_export

    async def run(self):
        company_internal_profiles = await self.company_internal_profiles_creator.get_company_internal_profiles()
        queried_company_internal_profiles = await self.query_profiles(company_internal_profiles)
        exported_internal_profiles_list = await self.company_profiles_export.export_company_internal_profiles(
            queried_company_internal_profiles
        )
        return exported_internal_profiles_list

    async def query_profiles(self, company_internal_profiles):
        queried_company_internal_profiles_list = []
        for company_profile in company_internal_profiles:
            company_profile = await self.db.query_company_profile_by_base_web_address(company_profile.base_web_address)
            if company_profile:
                queried_company_internal_profiles_list.append(CompanyInternalProfile.from_dict(company_profile))
        return queried_company_internal_profiles_list
