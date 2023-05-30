import asyncio
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorClientSession, AsyncIOMotorDatabase
from pymongo.errors import DocumentTooLarge
from load.models.company_internal_profile import CompanyInternalProfile
from load.mongodb.mongodb_base import MongoDBBase
from log.log_config import get_logger
from utils.constants import MongoDbConstants
from load.mongodb.mongo_db_config import MongoDbConfig
from utils.utils import get_date_now_timestamp, add_new_items_to_existing_company_internal_profile

DATA_INSERTED_SUCCESSFULLY = 'Data Inserted Successfully'
OOPS_ERROR = 'OOPS!! Some ERROR Occurred'


class MongoDBAsync(MongoDBBase):

    def __init__(self, mongodb_config: MongoDbConfig, base_collection_name, auth_source='admin'):
        self.my_logger = get_logger("MongoDBAsync")
        super().__init__(
            mongodb_config=mongodb_config,
            base_collection_name=base_collection_name,
            auth_source=auth_source
        )
        try:
            self.my_logger.debug('MongoDB Connection URI ' + str(self.uri))
            self.client: AsyncIOMotorClient = AsyncIOMotorClient(
                self.uri,
                ssl=mongodb_config.ssl,
            )
            self.client.get_io_loop = asyncio.get_running_loop
            self.db: AsyncIOMotorDatabase = self.client[self.db_name]
            self.session: AsyncIOMotorClientSession = None
            if self.client.server_info():
                self.my_logger.debug('MongoDB Connection Successful. CHEERS!!!')
        except Exception as e:
            self.my_logger.debug('Connection Unsuccessful!! ERROR!!')
            self.my_logger.debug(e)

    async def _get_all_collections_names(self):
        collection_names = await self.db.list_collection_names()
        for collection_name in collection_names:
            if self.base_collection_name in collection_name:
                yield collection_name

    async def _get_collection_name(self, company_base_web_address):
        index_table_postfix = self.base_collection_name + MongoDbConstants.MONGO_INDEX_TABLE_POSTFIX
        collection_name_dict = await self._query_by_base_web_address(
            index_table_postfix, company_base_web_address)
        if collection_name_dict:
            self.my_logger.debug('internal_collection_name_dict ' + str(collection_name_dict))
            return collection_name_dict[MongoDbConstants.INTERNAL_COLLECTION_NAME]
        return None

    async def query_company_profile_by_base_web_address(self, company_base_web_address):
        collection_name = await self._get_collection_name(company_base_web_address)
        return await self._query_by_base_web_address(collection_name, company_base_web_address)

    async def _query_by_base_web_address(self, collection, company_base_web_address):
        if not collection or not company_base_web_address:
            return None
        query = {"base_web_address": {"$eq": company_base_web_address}}
        try:
            data = await self.db[collection].find_one(query)
            self.my_logger.debug('query_db_profile_web_address_internal_collection_name Successfully')
            return data
        except Exception as e:
            self.my_logger.debug('_query_by_base_web_address Some ERROR Occurred')
            self.my_logger.debug(e)

    async def _insert_data_to_index_collection(
            self,
            collection_name,
            company_base_web_address
    ):
        index_collection_postfix = self.base_collection_name + MongoDbConstants.MONGO_INDEX_TABLE_POSTFIX
        web_address_collection_name_dict = {
            MongoDbConstants.BASE_WEB_ADDRESS: company_base_web_address,
            MongoDbConstants.INTERNAL_COLLECTION_NAME: collection_name
        }
        return await self._insert_data(index_collection_postfix, web_address_collection_name_dict)

    async def store_company_internal_profile_data(
            self,
            company_internal_profile
    ):
        company_base_web_address = company_internal_profile.base_web_address
        data = company_internal_profile.to_dict()
        collection_name = await self._get_collection_name(company_base_web_address)
        try:
            if collection_name:
                self.my_logger.debug('insert_company_profile_data: found existing collection name')
                await self._merge_profiles(collection_name, company_internal_profile)
                return await self._replace_profile(collection_name, company_internal_profile)
            else:
                for new_collection_name in self._get_new_collection_name(company_base_web_address):
                    if await self._insert_data(new_collection_name, data):
                        return await self._insert_data_to_index_collection(new_collection_name, company_base_web_address)
                    else:
                        return False
        except Exception as e:
            self.my_logger.debug(OOPS_ERROR + " in store_company_internal_profile_data")
            self.my_logger.debug(e)
        return False

    async def _insert_data(self, collection_name, data):
        self.my_logger.debug(f"collection_name {collection_name}")
        self.my_logger.debug("data " + str(data))
        try:
            res = await self.db[collection_name].insert_one(data)
            self.my_logger.debug(DATA_INSERTED_SUCCESSFULLY)
            if res:
                return True
        except Exception as e:
            self.my_logger.debug(OOPS_ERROR)
            self.my_logger.debug(e)
            if isinstance(e, DocumentTooLarge):
                raise DocumentTooLarge

    async def read_all_company_profiles(self):
        async for collection_name in self._get_all_collections_names():
            documents_list = await self.read_all_profiles_from_collection(collection_name)
            if documents_list:
                yield documents_list

    async def read_all_profiles_from_collection(self, collection_name):
        try:
            documents_list = await self.db[collection_name].find().sort("_id").to_list()
            self.my_logger.debug('Data read_from_db Successfully')
            return documents_list
        except Exception as e:
            self.my_logger.debug(OOPS_ERROR)
            self.my_logger.debug(e)

    async def update_latest_date_published(self, base_web_address):
        latest_date_published = get_date_now_timestamp()
        new_value = {
            '$set': {
                'latest_date_published': latest_date_published
            }
        }
        collection_name = await self._get_collection_name(base_web_address)
        return await self._update_company_profile(
            base_web_address,
            new_value,
            collection_name
        )

    async def update_language(self, company_internal_profile: CompanyInternalProfile):
        new_value = {
            '$set': {
                'language': company_internal_profile.language
            }
        }
        collection_name = await self._get_collection_name(company_internal_profile.base_web_address)
        return await self._update_company_profile(
            company_internal_profile.base_web_address,
            new_value,
            collection_name
        )

    async def _update_company_profile(self, base_web_address, new_values, collection):
        query = {
            "base_web_address": base_web_address,
        }
        try:
            data = await self.db[collection].update_one(query, new_values, upsert=False)
            self.my_logger.debug('Data update company internal profile Successfully')
            return data
        except Exception as e:
            self.my_logger.debug('update_company_internal_profile_language_internal_collection_name ERROR Occurred')
            self.my_logger.debug(e)

    async def drop_all_collections(self):
        async for collection_name in self._get_all_collections_names():
            await self.db.drop_collection(collection_name)

    async def _replace_profile(self, collection, company_internal_profile):
        data = company_internal_profile.to_dict()
        query = {"base_web_address": "company_internal_profile.base_web_address"}
        try:
            res = await self.db[collection].replace_one(query, data)
            self.my_logger.debug('Replace CompanyInternalProfile Successfully')
            return res
        except Exception as e:
            self.my_logger.debug('_replace_profile ERROR Occurred')
            self.my_logger.debug(e)
        return None

    async def _merge_profiles(self, collection, company_internal_profile):
        old_company_internal_profile_dict = None
        try:
            old_company_internal_profile_dict = await self._query_by_base_web_address(
                collection,
                company_internal_profile.base_web_address
            )
        except Exception as ex:
            self.my_logger.debug("_merge_profiles get old profile from db exception " + str(ex))
        old_company_internal_profile = None
        if old_company_internal_profile_dict:
            old_company_internal_profile = CompanyInternalProfile.from_dict(old_company_internal_profile_dict)
        if old_company_internal_profile:
            company_internal_profile = add_new_items_to_existing_company_internal_profile(
                company_internal_profile, old_company_internal_profile)
            if company_internal_profile:
                return company_internal_profile
        return None

    async def delete_company_profile_by_base_web_address(self, company_base_web_address):
        collection_name = await self._get_collection_name(company_base_web_address)
        await self._delete_profile_by_base_web_address(collection_name, company_base_web_address)

    async def _delete_profile_by_base_web_address(self, collection, company_base_web_address):
        if not collection or not company_base_web_address:
            return None
        query = {"base_web_address": {"$eq": company_base_web_address}}
        try:
            data = await self.db[collection].delete_one(query)
            self.my_logger.debug('_delete_profile_by_base_web_address Successfully')
            return data
        except Exception as e:
            self.my_logger.debug('_delete_profile_by_base_web_address Some ERROR Occurred')
            self.my_logger.debug(e)
