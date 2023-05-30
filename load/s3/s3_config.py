
class S3Config(object):

    aws_access_key_id: str
    aws_secret_key: str

    def __init__(self, json_object):
        self.aws_access_key_id = json_object['AWSAccessKeyId']
        self.aws_secret_access_key = json_object['AWSSecretKey']
