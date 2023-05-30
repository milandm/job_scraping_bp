class MongoDbConfig(object):
    server: str
    username: str
    password: str
    host: str
    port: int
    db_name: str
    ssl: bool

    def __init__(self, json_object):
        self.server = json_object['server']
        self.username = json_object['username']
        self.password = json_object['password']
        self.host = json_object['host']
        self.port = json_object['port']
        self.db_name = json_object['db_name']
        self.ssl = json_object['ssl']
