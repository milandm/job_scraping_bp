from load.mongodb.mongo_db_config import MongoDbConfig
from extract.models.csv_config import CsvConfig
from typing import List
from load.s3.s3_config import S3Config


class DataConfig(object):

    csv_files: List[CsvConfig]
    csv_resources_list: list
    mongo_db_config: MongoDbConfig
    s3_config: S3Config

    def __init__(self, json_object, db_config):
        self.csv_resources_list = list(
            map(lambda item: CsvConfig.from_dict(item), json_object['csv_resources_list'])
        )
        self.mongo_db_config = MongoDbConfig(json_object[db_config])
        self.s3_config = S3Config(json_object['s3_config'])
