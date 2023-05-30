from config.models.data_config import DataConfig
from load.mongodb.mongodb_async import MongoDBAsync
from load.mongodb.mongodb import MongoDB
from load.s3.s3_api import S3Api
from load.s3.s3_api_async import S3ApiAsync


def get_mongodb(config: DataConfig, base_collection_name) -> MongoDB:
    return MongoDB(
        mongodb_config=config.mongo_db_config,
        base_collection_name=base_collection_name
    )


def get_async_mongodb(config: DataConfig, base_collection_name) -> MongoDBAsync:
    return MongoDBAsync(
        mongodb_config=config.mongo_db_config,
        base_collection_name=base_collection_name
    )


def get_s3_obj(config: DataConfig, bucket_name) -> S3Api:
    return S3Api(bucket_name=bucket_name, config=config.s3_config)


def get_async_s3_obj(config: DataConfig, bucket_name) -> S3ApiAsync:
    return S3ApiAsync(bucket_name=bucket_name, config=config.s3_config)

