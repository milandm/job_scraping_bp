from abc import abstractmethod, ABC
from load.load import Load


class BaseStoreData(ABC):

    def __init__(
            self,
            data_source: str,
            mongo_db: Load,
    ):
        self.data_source = data_source
        self.db: Load = mongo_db

    @abstractmethod
    def store_profiles(self, company_internal_profiles_list):
        pass
