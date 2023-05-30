from load.models.company_internal_profile import CompanyInternalProfile
from log.log_config import get_logger
from transform.sources.linkedin_sales_navigator_transform import LinkedinSalesNavigatorTransform
from utils.constants import SourcesConstants


class Transform:

    def __init__(self):
        self.my_logger = get_logger("Transform")
        self.linkedin_sales_navigator_transform = LinkedinSalesNavigatorTransform()

    def get_transform(self, external_data_source):
        transform = {
            SourcesConstants.LINKEDIN_SALES_NAVIGATOR: self.linkedin_sales_navigator_transform,
        }
        return transform.get(external_data_source, "Invalid external_data_source")

    def get_company_internal_profile_from_external(self, external_profile_dictionary, external_data_source):
        transform = self.get_transform(external_data_source)
        return transform.get_company_internal_profile_from_external(external_profile_dictionary)

    async def async_get_company_internal_profile_from_external(self, external_profile_dictionary, external_data_source):
        transform = self.get_transform(external_data_source=external_data_source)
        return await transform.async_get_company_internal_profile_from_external(external_profile_dictionary)

    def company_internal_profile_to_csv(self, external_data_source, company_internal_profile: CompanyInternalProfile):
        self.my_logger.debug(f'company_internal_profile_to_csv ENTERED external_data_source {external_data_source}')
        transform = self.get_transform(external_data_source)
        return transform.company_internal_profile_to_csv(company_internal_profile)
