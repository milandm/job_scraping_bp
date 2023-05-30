import asyncio
from engines.company_internal_profiles_creator.base_company_internal_profile_creator import BaseCompanyInternalProfilesCreator
from extract.extract import Extract
from log.log_config import get_logger
from transform.transform import Transform


class AsyncCompanyInternalProfilesCreator(BaseCompanyInternalProfilesCreator):

    def __init__(self, data_source: str, extract: Extract):
        super().__init__(data_source, extract)
        self.logger = get_logger('AsyncCompanyInternalProfilesCreator')

    async def get_company_internal_profiles(self):
        companies_external_data_list = self.extract.extract_data()
        return await self._create_company_internal_profiles(companies_external_data_list)

    async def _create_company_internal_profiles(self, companies_external_data_list):
        create_internal_profiles_tasks = self._get_create_internal_profiles_tasks(companies_external_data_list)
        return await asyncio.gather(*create_internal_profiles_tasks)

    def _get_create_internal_profiles_tasks(self, external_company_profiles_list):
        transform = Transform()
        create_internal_profiles_tasks = []
        for external_profile_dict in external_company_profiles_list:
            task = transform.async_get_company_internal_profile_from_external(
                external_profile_dictionary=external_profile_dict,
                external_data_source=self.data_source
            )
            create_internal_profiles_tasks.append(task)
        return create_internal_profiles_tasks
