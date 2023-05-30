from load.s3.s3_api_base import S3ApiBase
from log.log_config import get_logger
import boto3
from boto3.s3.transfer import TransferConfig
from load.s3.s3_config import S3Config


class S3Api(S3ApiBase):

    def __init__(self, bucket_name, config: S3Config):
        self.logger = get_logger('S3Api')
        self.s3 = boto3.resource(
            's3',
            aws_access_key_id=config.aws_access_key_id,
            aws_secret_access_key=config.aws_secret_access_key,
            verify=True
        )
        self.bucket_name = bucket_name
        self.config = TransferConfig(
            multipart_threshold=1024,
            max_concurrency=5,
            multipart_chunksize=1024,
            use_threads=True
        )

    def set_bucket_name(self, bucket_name):
        self.bucket_name = bucket_name

    def put(self, data, key, metadata=None):
        if not metadata:
            metadata = {}
        if data and key:
            try:
                self.logger.debug(f'put object key: {key}')
                bucket = self.load_bucket()
                bucket.put_object(Body=data, Key=key, Metadata=metadata)
                return self.check_if_exists(key, bucket)
            except Exception as e:
                self.logger.error(f'Exception uploading object to s3 {e}')
        return False

    def upload_file_object(self, file_path, key, metadata=None):
        if not metadata:
            metadata = {}
        try:
            bucket = self.load_bucket()
            if metadata:
                bucket.upload_fileo(Filename=file_path, Key=key,
                                    ExtraArgs={"Metadata": metadata})
            else:
                bucket.upload_file(Filename=file_path, Key=key)
        except Exception as e:
            self.logger.error(f'Exception upload_file_object to s3 {e}')

    def load_bucket(self):
        try:
            buckets_list = self.get_current_bucket_list()
            buckets_list = list(map(lambda obj: obj.name, buckets_list))
            if self.bucket_name in buckets_list:
                self.logger.debug(f'Loading bucket: {self.bucket_name}')
                return self.s3.Bucket(self.bucket_name)
            else:
                self.logger.debug(f'Creating bucket: {self.bucket_name}')
                return self.create_bucket()
        except Exception as e:
            self.logger.debug(f'load_bucket exception: {e}')
        return None

    def get_object(self, key):
        content_object = self.s3.Object(self.bucket_name, key)
        file_content = content_object.get()['Body'].read().decode('utf-8')
        return file_content

    def check_if_exists(self, key, bucket):
        try:
            objs = list(bucket.objects.filter(Prefix=key))
            keys = set(o.key for o in objs)
            if key in keys:
                return True
        except Exception as e:
            self.logger.debug(f'Exception in check_if_exists: {e}')
            return False
        return False

    def get_current_bucket_list(self):
        bucket_list = list()
        for bucket_ in self.s3.buckets.all():
            bucket_list.append(bucket_)
        return bucket_list

    def create_bucket(self):
        return self.s3.create_bucket(
            Bucket=self.bucket_name,
            CreateBucketConfiguration={
                "LocationConstraint": "eu-west-1"
            },
        )
