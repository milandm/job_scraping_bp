from abc import ABC, abstractmethod


class S3ApiBase(ABC):

    @abstractmethod
    def put(self, data, key, metadata):
        pass

    @abstractmethod
    def upload_file_object(self, file_path, key, metadata):
        pass

    @abstractmethod
    def load_bucket(self):
        pass

    @abstractmethod
    def get_object(self, key):
        pass
