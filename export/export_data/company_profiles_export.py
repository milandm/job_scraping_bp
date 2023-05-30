from export.data_export import DataExport
from log.log_config import get_logger
from load.s3.s3_api import S3Api
from export.export_data.company_profiles_export_base import CompanyProfilesExportBase


class CompanyProfilesExport(CompanyProfilesExportBase):

    def __init__(
            self,
            data_source: str,
            db,
            s3: S3Api,
            data_export: DataExport
    ):
        self.logger = get_logger('CompanyProfilesExport')
        self.data_source = data_source
        self.db = db
        self.s3 = s3
        self.data_export = data_export

    def export_company_internal_profiles(self, company_internal_profiles_list):
        exported_profiles = self.data_export.export_companies_data(company_internal_profiles_list)
        self.store_file_to_s3()
        self.add_latest_date_published(exported_profiles)
        return exported_profiles

    def store_file_to_s3(self):
        key = self.data_export.file_path.split('/')[-1]
        try:
            self.s3.upload_file_object(file_path=self.data_export.file_path, key=key)
        except Exception as e:
            self.logger.debug(f'Exception: {e}')

    def add_latest_date_published(self, exported_profiles):
        self.logger.debug('add_latest_date_published ENTERED')
        for company_internal_profile in exported_profiles:
            self.db.update_latest_date_published(company_internal_profile.base_web_address)
        self.logger.debug('add_latest_date_published done')
