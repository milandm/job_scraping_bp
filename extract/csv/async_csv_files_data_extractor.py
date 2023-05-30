from typing import List
from extract.extract import Extract
from extract.models.csv_config import CsvConfig
from log.log_config import get_logger
from utils.utils import fetch_csv_sources_and_files
from extract.utils.csv_file_reader import CsvFileReader


class AsyncCsvFilesDataExtractor(Extract):
    """Class to extract company external profile dicts from csv files of a given directory"""
    def __init__(self, data_source, files_dir, delimiter=','):
        self.my_logger = get_logger("AsyncCsvFilesDataExtractor")
        self.data_source = data_source
        self.files_dir = files_dir
        self.delimiter = delimiter

    async def extract_data(self) -> List[dict]:
        """Reads content of a csv file and returns list of company external profiles"""
        pass

    async def get_csv_files_paths(self):
        """Fetches all files from directory"""
        pass

    def get_external_data_dicts_from_path_list(self, csv_files_path_list):
        # should be implemented
        pass
