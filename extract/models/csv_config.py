class CsvConfig(object):
    source_name: str
    file_path_url: str
    source_type: str

    def __init__(
            self,
            source_name: str = None,
            file_path_url: str = None,
            source_type: str = None
    ):
        self.source_name = source_name
        self.file_path_url = file_path_url
        self.source_type = source_type

    @classmethod
    def from_dict(cls, json_object):
        return cls(source_name=json_object.get('source_name', ''),
                   file_path_url=json_object.get('file_path_url', ''),
                   source_type=json_object.get('source_type', ''))

    def __str__(self):
        return f'source_name: {self.source_name},' \
               f'file_path_url: {self.file_path_url},' \
               f'source_type: {self.source_type}'

    def __repr__(self):
        return self.__str__()
