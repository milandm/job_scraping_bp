from load.s3.s3_config import S3Config
from log.log_config import get_logger
import aioboto3
from load.s3.s3_api_base import S3ApiBase


class S3ApiAsync(S3ApiBase):

    def __init__(self, bucket_name, config: S3Config):
        self.logger = get_logger('S3ApiAsync')
        self.session = aioboto3.Session()
        self.bucket_name = bucket_name
        self.aws_access_key_id = config.aws_access_key_id
        self.aws_secret_access_key = config.aws_secret_access_key

    async def put(self, data, key, metadata):
        if not metadata:
            metadata = {}
        async with self.session.resource(
                "s3",
                aws_access_key_id=self.aws_access_key_id,
                aws_secret_access_key=self.aws_secret_access_key,
                verify=True
        ) as s3:
            try:
                bucket = await self.load_bucket(s3_resource=s3)
                await bucket.put_object(Body=data, Key=key, Metadata=metadata)
            except Exception as e:
                self.logger.error(f'Exception uploading file to s3 {e}')

    async def upload_file_object(self, file_path, key, metadata=None):
        if not metadata:
            metadata = {}
        async with self.session.client(
                "s3",
                aws_access_key_id=self.aws_access_key_id,
                aws_secret_access_key=self.aws_secret_access_key,
                verify=False
        ) as s3:
            try:
                with open(file_path, 'rb') as f:
                    await s3.upload_fileobj(f, self.bucket_name, key, ExtraArgs={"Metadata": metadata})
            except Exception as e:
                self.logger.error(f'Exception uploading file to s3 {e}')

    async def load_bucket(self, s3_resource):
        try:
            buckets_list = self.get_current_bucket_list(s3_resource)
            if self.bucket_name in buckets_list:
                self.logger.debug(f'loading bucket: {self.bucket_name}')
                return await s3_resource.Bucket(self.bucket_name)
            else:
                self.logger.debug(f'Creating bucket: {self.bucket_name}')
                return await self.create_bucket(s3_resource)
        except Exception as e:
            self.logger.debug(f'load_bucket exception: {e}')
        return None

    async def get_object(self, key):
        async with self.session.resource(
                "s3",
                aws_access_key_id=self.aws_access_key_id,
                aws_secret_access_key=self.aws_secret_access_key,
                verify=False
        ) as s3:
            bucket = await self.load_bucket(s3_resource=s3)
            blob_object = bucket.get_object(Key=key)
            return blob_object

    async def get_current_bucket_list(self, s3):
        bucket_list = list()
        for bucket in s3.buckets.all():
            bucket_list.append(bucket)
        return bucket_list

    async def create_bucket(self, s3):
        return await s3.create_bucket(
            Bucket=self.bucket_name,
            CreateBucketConfiguration={
                "LocationConstraint": "eu-west-1"
            }
        )
