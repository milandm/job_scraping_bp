from itertools import compress
import asyncio
from load.store_company_internal_profiles.base_store_data import BaseStoreData
from load.mongodb.mongodb_async import MongoDBAsync
from load.load import Load
from log.log_config import get_logger


class AsyncStoreData(BaseStoreData):

    def __init__(
            self,
            data_source: str,
            db: Load
    ):
        super().__init__(data_source, db)
        self.logger = get_logger('StoreCsvDataEngine')

    async def store_profiles(self, company_internal_profiles_list):
        store_profiles_task_list = self.get_store_profiles_tasks(company_internal_profiles_list)
        stored_profiles_filter = await asyncio.gather(*store_profiles_task_list)
        return list(compress(company_internal_profiles_list, stored_profiles_filter))

    def get_store_profiles_tasks(self, company_internal_profiles_list):
        store_task_list = []
        if isinstance(self.db, MongoDBAsync):
            for company_profile in company_internal_profiles_list:
                task = self.db.store_company_internal_profile_data(
                    company_internal_profile=company_profile
                )
                store_task_list.append(task)
        else:
            self.logger('You are using NOT async db instance with async method')
        return store_task_list
