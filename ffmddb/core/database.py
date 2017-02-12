import contextlib
import yaml

from ffmddb.core.models.config import Configuration
from ffmddb.core.models.index import CoreIndex


class Database:
    """Stores a reference to a database (a configuration file and the files it
    specifies), providing methods to interact with it
    """

    def __init__(self, config_obj, config_file=None):
        """TODO"""
        self.config = config_obj
        self.config_file = config_file
        self.core_index = CoreIndex()
        self.core_index.load(self.config.options['indices_location'])

    def sync(self):
        """TODO"""
        pass

    def get_documents(self, collection_name, query):
        """TODO"""
        pass

    def update_document(self, document, field, value):
        """TODO"""
        pass

    def delete_document(self, document):
        """TODO"""
        pass

    def create_document(self, document):
        """TODO"""
        pass

    def get_collection(self, name):
        """TODO"""
        pass

    def delete_collection(self, name, cascade=False):
        """TODO"""
        pass

    def create_collection(self, name, path, mkdir_if_needed=True,
                          keep_file=True):
        """TODO"""
        pass

    @contextlib.contextmanager
    def committing(self):
        """TODO"""
        yield
        self.commit()

    def commit(self):
        """TODO"""
        for index in self.indices:
            index.write()
        self.core_index.write()

    @contextlib.contextmanager
    def closing(self):
        """TODO"""
        yield
        self.close()

    def close(self):
        """TODO"""
        for index in self.indices:
            index.close()
        self.core_index.close()
        self.config.close(self.config_file)

    @classmethod
    def from_file(cls, config_file):
        """TODO"""
        with open(config_file) as f:
            config_str = f.read()
        return Database.from_string(config_str, config_file=config_file)

    @classmethod
    def from_string(cls, config_str, config_file=None):
        """TODO"""
        config = Configuration.from_object(yaml.safe_load(config_str))
        return Database(config, config_file=config_file)
