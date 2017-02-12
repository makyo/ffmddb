import os
import re
import yaml

from ffmddb.core.models.field import Field


NEWLINES = re.compile(r'\n\n+')


class Collection:
    """Stores a reference to a collection of documents"""

    def __init__(self, name, path):
        """TODO"""
        self.name = name
        self.path = path

    def marshal(self):
        """TODO"""
        return {'name': self.name, 'path': self.path}


class CollectionField:
    """Stores an abstract reference to a field which should exist on most/all
    documents in a collection, used for indexing
    """

    def __init__(self, collection, field):
        """TODO"""
        self.collection = collection
        self.field = field

    def marshal(self):
        """TODO"""
        return [self.collection.name, self.field.marshal()]


class Document:
    """Stores a reference to a single document"""

    def __init__(self, db, collection, name, document_field=None,
                 metadata=None):
        self.db = db
        self._collection = collection
        self._name = name
        self._document_field = document_field
        self._metadata = metadata
        self.valid = None
        self.changed = False

    def update(self, field, value):
        """TODO"""
        if isinstance(field, str):
            field = Field(field)
        self.changed = True
        field.set(document, value)

    def marshal(self):
        """TODO"""
        pass

    def read(self):
        """TODO"""
        self.valid = False
        with open(os.path.join(self._collection.path,
                  self.name), 'r') as f:
            collecting = False
            collected = False
            done = False
            document_field = ""
            metadata_string = ""
            open_fence = re.compile(self.db.config.options['fence'][0])
            close_fence = re.compile(self.db.config.options['fence'][1])
            for line in f:
                if not done:
                    if not collecting and open_fence.match(line.strip()):
                        collecting = True
                        collected = True
                        continue
                    if collecting and close_fence.match(line.strip()):
                        collecting = False
                        done = (collected and not
                                self.db.config.options['multiple_metadata'])
                        continue
                if collecting:
                    metadata_string += line
                else:
                    document_field += line
            self._document_field = document_field
            self._metadata = {}
            if collected:
                self._metadata = yaml.safe_load(
                    NEWLINES.sub('', metadata_string))
            if len(self.metadata) > 0:
                self.valid = True
