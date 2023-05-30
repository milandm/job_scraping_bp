from abc import ABC
from abc import abstractmethod


class CompanyProfilesExportBase(ABC):

    @abstractmethod
    def export_company_internal_profiles(self, company_internal_profiles_list):
        pass

    @abstractmethod
    def store_file_to_s3(self):
        pass

    @abstractmethod
    def add_latest_date_published(self, exported_profiles):
        pass
