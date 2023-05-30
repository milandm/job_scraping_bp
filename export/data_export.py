from abc import ABC, abstractmethod
from typing import List
from load.models.company_internal_profile import CompanyInternalProfile


class DataExport(ABC):

    def __init__(self, data_source, file_path):
        self.data_source = data_source
        self.file_path = file_path

    @abstractmethod
    def export_companies_data(self, company_internal_profiles: List[CompanyInternalProfile]):
        pass
