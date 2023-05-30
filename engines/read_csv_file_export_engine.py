from extract.csv.csv_files_data_extractor import CsvFilesDataExtractor
from load.models.company_internal_profile import CompanyInternalProfile
from load.mongodb.mongodb import MongoDB
from log.log_config import get_logger
from export.export_data.company_profiles_export import CompanyProfilesExport
from engines.company_internal_profiles_creator.company_internal_profile_creator import CompanyInternalProfilesCreator


class ReadCsvFilesExportEngine:
    def __init__(
            self,
            data_source,
            db: MongoDB,
            company_profiles_export: CompanyProfilesExport,
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
        self.db = db
        self.company_profiles_export = company_profiles_export

    def run(self):
        company_internal_profiles = self.company_internal_profiles_creator.get_company_internal_profiles()
        stored_company_internal_profiles = self.query_stored_profiles(company_internal_profiles)
        exported_internal_profiles_list = self.company_profiles_export.export_company_internal_profiles(
            stored_company_internal_profiles
        )
        return exported_internal_profiles_list

    def query_stored_profiles(self, company_internal_profiles):
        queried_company_internal_profiles_list = []
        for company_profile in company_internal_profiles:
            company_profile = self.db.query_company_profile_by_base_web_address(company_profile.base_web_address)
            if company_profile:
                company_internal_profile = CompanyInternalProfile.from_dict(company_profile)
                queried_company_internal_profiles_list.append(company_internal_profile)
        return queried_company_internal_profiles_list
