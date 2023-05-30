from load.store_company_internal_profiles.base_store_data import BaseStoreData
from load.load import Load
from log.log_config import get_logger
from itertools import compress


class StoreData(BaseStoreData):

    def __init__(
            self,
            data_source: str,
            db: Load
    ):
        super().__init__(data_source, db)
        self.logger = get_logger('ReadCsvDataEngine')

    def store_profiles(self, company_internal_profiles_list):
        stored_profiles_filter = []
        for company_profile in company_internal_profiles_list:
            stored_profiles_filter.append(self.db.store_company_internal_profile_data(
                company_internal_profile=company_profile
            ))
        return list(compress(company_internal_profiles_list, stored_profiles_filter))
