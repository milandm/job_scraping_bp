from typing import List
from extract.extract import Extract
from extract.models.csv_config import CsvConfig
from log.log_config import get_logger
from utils.utils import fetch_csv_sources_and_files
from extract.utils.csv_file_reader import CsvFileReader


class CsvFilesDataExtractor(Extract):
    """Class to extract company external profile dicts from csv files of a given directory"""
    def __init__(self, data_source, files_dir, delimiter=','):
        self.my_logger = get_logger("CsvFilesDataExtractor")
        self.data_source = data_source
        self.files_dir = files_dir
        self.delimiter = delimiter

    def extract_data(self) -> List[dict]:
        """Reads content of a csv file and returns list of company external profiles"""
        csv_files_path_list = self.get_csv_files_paths()
        return self.get_external_data_dicts_from_path_list(csv_files_path_list)

    def get_csv_files_paths(self):
        """Fetches all files from directory"""
        csv_files_sources_list = fetch_csv_sources_and_files(self.files_dir)
        csv_files_list = list(
            map(
                lambda csv_file_source: CsvConfig(source_name=csv_file_source[0], file_path_url=csv_file_source[1]),
                csv_files_sources_list
            )
        )
        return csv_files_list

    def get_external_data_dicts_from_path_list(self, csv_files_path_list):
        companies_external_data_list = []
        csv_file_reader = CsvFileReader()
        for file_path in csv_files_path_list:
            companies_external_data_list += csv_file_reader.read_data(
                file_path_or_url=file_path.file_path_url,
                delimiter=self.delimiter
            )
        return companies_external_data_list
