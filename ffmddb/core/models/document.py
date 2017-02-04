import os
import yaml


class Collection:
    """Stores a reference to a collection of documents"""

    def __init__(self, name, path):
        self.name = name
        self.path = path

    def marshal(self):
        return {'name': self.name, 'path': self.path}


class CollectionField:
    """Stores an abstract reference to a field which should exist on most/all
    documents in a collection, used for indexing
    """

    def __init__(self, collection, field):
        self.collection = collection
        self.field = field

    def marshal(self):
        return [self.collection.name, self.field.value]


class Document:
    """Stores a reference to a single document"""

    def __init__(self, db, collection, name, document_field=None,
                 metadata=None):
        self.db = db
        self.collection = collection
        self.name = name
        self.document_field = document_field
        self.metadata = metadata
        self.valid = None

    def marshal(self):
        pass

    def _read(self):
        self.valid = False
        with open(os.path.join(self.collection.path,
                  self.document.name), 'r') as f:
            metadata_collecting = False
            document_field = ""
            metadata_string = ""
            for line in f:
                if line.strip() == self.db.config.options['fence'][0]:
                    metadata_collecting = True
                    continue
                if line.strip() == self.db.config.options['fence'][1] and \
                        metadata_collecting:
                    metadata_collecting = False
                    continue
                if metadata_collecting:
                    metadata_string += line
                else:
                    document_field += line
            self.document_field = document_field
            metadata = yaml.safe_load(metadata_string)
            self.metadata = metadata
            if len(self.metadata) > 0:
                self.valid = True
