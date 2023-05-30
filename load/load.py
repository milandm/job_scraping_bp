from abc import ABC, abstractmethod
from load.models.company_internal_profile import CompanyInternalProfile


class Load(ABC):

    @abstractmethod
    def store_company_internal_profile_data(
        self,
        company_internal_profile: CompanyInternalProfile
    ):
        pass

    @abstractmethod
    def read_all_company_profiles(self):
        pass

    @abstractmethod
    def query_company_profile_by_base_web_address(
            self,
            company_base_web_address
    ):
        pass

    @abstractmethod
    def delete_company_profile_by_base_web_address(
            self,
            company_base_web_address
    ):
        pass

    @abstractmethod
    def update_latest_date_published(self, company_internal_profile: CompanyInternalProfile):
        pass

    @abstractmethod
    def update_language(self, company_internal_profile: CompanyInternalProfile):
        pass
