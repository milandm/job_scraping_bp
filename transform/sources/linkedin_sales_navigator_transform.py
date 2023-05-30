from log.log_config import get_logger
from transform.sources.sources_transform_base import SourcesTransformBase
from load.models.company_internal_profile import CompanyInternalProfile
from utils.constants import SourcesConstants, CsvExportProfilePreviewConstants, CriterionLabelConstants, \
    DuplicateConstants
from utils.sources_constants import LinkedinSalesNavigatorExternalProfileConstants, \
    LinkedinSalesNavigatorInternalProfileConstants
from utils.utils import get_domain_from_url, async_get_domain_from_url, get_affinity_label


class LinkedinSalesNavigatorTransform(SourcesTransformBase):

    def __init__(self):
        self.my_logger = get_logger("LinkedinSalesNavigatorTransform")

    async def get_criterion_value_label(self, criterion_name, company_internal_profile):
        """will be implemented"""
        pass

    def get_companies_list_dates(self, company_internal_profile_list):
        """will be implemented"""
        pass

    def convert_text_content_csv_to_dict(self, external_profile_dictionary):
        """will be implemented"""
        pass

    def get_web_pages_text_content_list(self, external_profile_dictionary):
        """will be implemented"""
        pass

    def get_company_internal_profile_from_external(self, external_profile_dictionary):
        website_raw = external_profile_dictionary.get(LinkedinSalesNavigatorExternalProfileConstants.WEBSITE, '')
        try:
            base_web_address = get_domain_from_url(website_raw, self.my_logger)
            return self.create_company_internal_profile_from_external(external_profile_dictionary, base_web_address)
        except Exception as e:
            self.my_logger.debug(e)
            return CompanyInternalProfile()

    async def async_get_company_internal_profile_from_external(self, external_profile_dictionary):
        website_raw = external_profile_dictionary.get(LinkedinSalesNavigatorExternalProfileConstants.WEBSITE, '')
        try:
            base_web_address = await async_get_domain_from_url(website_raw, self.my_logger)
            return self.create_company_internal_profile_from_external(external_profile_dictionary, base_web_address)
        except Exception as e:
            self.my_logger.debug(e)
            return CompanyInternalProfile()

    def create_company_internal_profile_from_external(self, external_profile_dictionary, base_web_address):
        self.my_logger.debug(f'creating internal profile for: {base_web_address}')
        name_raw = external_profile_dictionary.get(LinkedinSalesNavigatorExternalProfileConstants.NAME, '')
        website_raw = external_profile_dictionary.get(LinkedinSalesNavigatorExternalProfileConstants.WEBSITE, '')
        location_raw = external_profile_dictionary.get(LinkedinSalesNavigatorExternalProfileConstants.LOCATION, '')
        industry_raw = external_profile_dictionary.get(LinkedinSalesNavigatorExternalProfileConstants.INDUSTRY, '')
        linkedin_url_raw = external_profile_dictionary.get(LinkedinSalesNavigatorExternalProfileConstants.LINKEDIN_URL, '')
        internal_linkedin_sales_nav_profile_dictionary = {
            LinkedinSalesNavigatorInternalProfileConstants.NAME: name_raw,
            LinkedinSalesNavigatorInternalProfileConstants.WEBSITE: website_raw,
            LinkedinSalesNavigatorInternalProfileConstants.LOCATION: location_raw,
            LinkedinSalesNavigatorInternalProfileConstants.INDUSTRY: industry_raw,
            LinkedinSalesNavigatorInternalProfileConstants.LINKEDIN_URL: linkedin_url_raw,
        }
        if external_profile_dictionary is not None:
            return CompanyInternalProfile(
                company_name=name_raw,
                full_web_address=website_raw,
                base_web_address=base_web_address,
                company_internal_items=list(),
                company_external_items_dict={
                    SourcesConstants.LINKEDIN_SALES_NAVIGATOR: internal_linkedin_sales_nav_profile_dictionary},
                language=None,
                company_internal_item_predictions_dict=dict(),
                company_internal_item_labels_dict=dict(),
                source_data_created_date=''
            )
        else:
            return CompanyInternalProfile()

    def company_internal_profile_to_csv(self, company_internal_profile: CompanyInternalProfile):
        self.my_logger.debug('LinkedinSalesNavigator company_internal_profile_to_csv ENTERED')
        profile_dict = dict()
        profile_dict[CsvExportProfilePreviewConstants.COMPANY_NAME] = company_internal_profile.company_name
        profile_dict[CsvExportProfilePreviewConstants.WEB_ADDRESS] = company_internal_profile.full_web_address
        profile_dict[CsvExportProfilePreviewConstants.AFFINITY_PRESENCE] = get_affinity_label(company_internal_profile)
        location = company_internal_profile.company_external_items_dict[SourcesConstants.LINKEDIN_SALES_NAVIGATOR].get(
            LinkedinSalesNavigatorInternalProfileConstants.LOCATION, "")
        profile_dict[CsvExportProfilePreviewConstants.LOCATION] = location
        if company_internal_profile.company_external_items_dict:
            duplicate_key = DuplicateConstants.NO
            if len(company_internal_profile.company_external_items_dict.keys()) > 1:
                duplicate_key = DuplicateConstants.YES
            profile_dict[CsvExportProfilePreviewConstants.DUPLICATE] = duplicate_key

        for criterion_name, criterion_preview_label in CsvExportProfilePreviewConstants.CRITERION_LABEL_CSV_EXPORT.items():
            company_internal_item_prediction = company_internal_profile.company_internal_item_predictions_dict.get(
                criterion_name, None)
            if company_internal_item_prediction:
                criterion_export_label = CriterionLabelConstants.CRITERION_EXPORT_LABEL.get(criterion_name, None)
                if criterion_export_label:
                    profile_dict[criterion_preview_label] = criterion_export_label.get(
                        company_internal_item_prediction.criterion_value_label, "")
            else:
                profile_dict[criterion_preview_label] = ''
        return profile_dict
