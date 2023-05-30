from abc import ABC, abstractmethod


class SourcesTransformBase(ABC):

    @abstractmethod
    def get_company_internal_profile_from_external(self, external_profile_dictionary):
        pass

    @abstractmethod
    async def get_criterion_value_label(self, criterion_name, company_internal_profile):
        pass

    @abstractmethod
    def get_companies_list_dates(self, company_internal_profile_list):
        pass

    @abstractmethod
    def convert_text_content_csv_to_dict(self, external_profile_dictionary):
        pass

    @abstractmethod
    def get_web_pages_text_content_list(self, external_profile_dictionary):
        pass

    @abstractmethod
    async def async_get_company_internal_profile_from_external(self, external_profile_dictionary):
        pass
