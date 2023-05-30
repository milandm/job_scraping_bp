from engines.company_internal_profiles_creator.base_company_internal_profile_creator import BaseCompanyInternalProfilesCreator
from log.log_config import get_logger
from transform.transform import Transform
from extract.extract import Extract


class CompanyInternalProfilesCreator(BaseCompanyInternalProfilesCreator):

    def __init__(self, data_source, extract: Extract):
        super().__init__(data_source, extract)
        self.logger = get_logger('CompanyInternalProfilesCreator')

    def get_company_internal_profiles(self):
        companies_external_data_list = self.extract.extract_data()
        return self._create_company_internal_profiles(companies_external_data_list)

    def _create_company_internal_profiles(self, external_profiles_list):
        transform = Transform()
        internal_profiles_list = []
        for external_profile_dict in external_profiles_list:
            company_internal_profile = transform.get_company_internal_profile_from_external(
                external_profile_dictionary=external_profile_dict,
                external_data_source=self.data_source
            )
            internal_profiles_list.append(company_internal_profile)
        return internal_profiles_list
