from abc import abstractmethod, ABC
from typing import List
from extract.csv.csv_files_data_extractor import CsvFilesDataExtractor
from extract.extract import Extract
from load.models.company_internal_profile import CompanyInternalProfile


class BaseCompanyInternalProfilesCreator(ABC):

    def __init__(
            self,
            data_source: str,
            extract: Extract
    ):
        self.data_source = data_source
        self.extract = extract

    @abstractmethod
    def get_company_internal_profiles(self) -> List[CompanyInternalProfile]:
        pass

    @abstractmethod
    def _create_company_internal_profiles(self, external_profiles_list):
        pass
