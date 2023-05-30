from abc import ABC
from abc import abstractmethod

from load.load import Load
from load.models.company_internal_profile import CompanyInternalProfile
from utils.utils import remove_non_alpha


class MongoDBBase(Load):

    def __init__(self, mongodb_config, base_collection_name, auth_source):
        self.base_collection_name = base_collection_name
        self.server = mongodb_config.server
        self.user = mongodb_config.username
        self.password = mongodb_config.password
        self.host = mongodb_config.host
        self.port = mongodb_config.port
        self.db_name = mongodb_config.db_name
        self.auth_source = auth_source
        self.uri = self.server + self.user + ':' + self.password + '@' + self.host + '/' + self.db_name + '?retryWrites=true&w=majority'

    @abstractmethod
    def _get_all_collections_names(self):
        pass

    @abstractmethod
    def _get_collection_name(self, company_base_web_address):
        pass

    @abstractmethod
    def _query_by_base_web_address(self, collection, company_base_web_address):
        pass

    @abstractmethod
    def _insert_data_to_index_collection(
            self,
            collection_name,
            company_base_web_address
    ):
        pass

    @abstractmethod
    def _insert_data(self, collection_name, data):
        pass

    @abstractmethod
    def read_all_profiles_from_collection(self, collection_name):
        pass

    @abstractmethod
    def drop_all_collections(self):
        pass

    def _get_new_collection_name(self, company_base_web_address):
        www_removed_substring = company_base_web_address.replace("www.", "")
        substring_cleaned = remove_non_alpha(www_removed_substring)
        substring_start = 0
        for i in range(len(substring_cleaned)):
            substring_end = i + 1
            substring = substring_cleaned[substring_start:substring_end]
            next_internal_collection_name = self.base_collection_name + "_" + substring
            yield next_internal_collection_name

    @abstractmethod
    def _update_company_profile(self, base_web_address, new_values, collection):
        pass

    @abstractmethod
    def _replace_profile(self, collection, company_internal_profile: CompanyInternalProfile):
        pass

    @abstractmethod
    def _merge_profiles(self, collection, company_internal_profile):
        pass
