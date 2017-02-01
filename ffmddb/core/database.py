import yaml

from ffmddb.core.models.config import Configuration


class Database:
    """Stores a reference to a database (a configuration file and the files it
    specifies), providing methods to interact with it
    """

    def __init__(self, config_obj, config_file=None):
        self.config = config_obj
        self.config_file = config_file

    def get_documents(self, collection_name, query):
        pass

    def update_document(self, document, field, value):
        pass

    def delete_document(self, document):
        pass

    def create_document(self, document):
        pass

    def get_collection(self, name):
        pass

    def delete_collection(self, name, cascade=False):
        pass

    def create_collection(self, name, path, mkdir_if_needed=True,
                          keep_file=True):
        pass

    def close(self):
        if self.config_file:
            config_str = self.config.marshal()
            with open(self.config_file, 'w') as f:
                f.write(config_str)

    @classmethod
    def from_file(cls, config_file):
        with open(config_file) as f:
            config_str = f.read()
        return Database.from_string(config_str, config_file=config_file)

    @classmethod
    def from_string(cls, config_str, config_file=None):
        config = Configuration.from_object(yaml.safe_load(config_str))
        return Database(config, config_file=config_file)
