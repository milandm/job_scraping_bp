from extract.extract import Extract
from log.log_config import get_logger
import pandas as pd


class CsvFileReader:

    def __init__(self):
        self.my_logger = get_logger('CsvFileReader')

    def read_data(self, file_path_or_url, delimiter=','):
        """Reads data from csv file and returns list of dictionaries.
        Can handle local files or remote files from url"""
        csv_data = list()
        try:
            self.my_logger.debug(f'file path or url: {file_path_or_url}')
            df = pd.read_csv(file_path_or_url, sep=delimiter)
            list_of_rows = [list(row) for row in df.values]
            list_of_rows.insert(0, df.columns.to_list())
            header = list_of_rows[0]
            for row_index in range(1, len(list_of_rows)):
                row_dict = dict()
                row = list_of_rows[row_index]
                for element_index in range(len(row)):
                    row_dict[header[element_index]] = row[element_index]
                csv_data.append(row_dict)
            return csv_data
        except Exception as e:
            self.my_logger.debug(f'read_data exception: {e}')
            return csv_data
