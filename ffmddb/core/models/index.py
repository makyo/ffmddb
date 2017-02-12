import os
import yaml


class Index:
    """Provides an interface of common methods for collection types"""

    def read(self):
        """TODO"""
        try:
            with open(self.filename, 'rb') as f:
                contents = f.read()
        except FileNotFoundError:
            contents = ''
        self.raw_data = yaml.safe_load(contents)

    def write(self):
        """TODO"""
        with open(self.filename, 'wb') as f:
            f.write(yaml.safe_dump(self.raw_data))

    def close(self):
        """TODO"""
        # TODO should probably run additional checks for consistency.
        self.write(self.marshal_contents())


class SingleCollectionIndex(Index):
    """Represents an index on one field common to a collection"""

    def __init__(self, name, collection_field):
        """TODO"""
        self.name = name
        self.collection_field = collection_field

    def load(self, indices_dir):
        """TODO"""
        self.read(os.path.join(indices_dir, '{}.yaml'.format(self.name)))

    def marshal(self):
        """TODO"""
        return {
            'name': self.name,
            'from': self.collection_field.marshal(),
        }


class CrossCollectionIndex(Index):
    """Represents an index on one field common to a collection which maps to a
    field on another (or the same) collection
    """

    def __init__(self, name, from_collection_field, to_collection_field):
        """TODO"""
        self.name = name
        self.from_collection_field = from_collection_field
        self.to_collection_field = to_collection_field

    def load(self, indices_dir):
        """TODO"""
        self.read(os.path.join(indices_dir, '{}.yaml'.format(self.name)))

    def marshal(self):
        """TODO"""
        return {
            'name': self.name,
            'from': self.from_collection_field.marshal(),
            'to': self.to_collection_field.marshal(),
        }


class CoreIndex(Index):
    """Represents the core index, which tracks documents and metadata field
    names, as well as indices
    """

    def __init__(self):
        """TODO"""
        self.indices = {}
        self.documents = {}

    def load(self, indices_dir):
        """TODO"""
        self.read(os.path.join(indices_dir, '_core_idx.yaml'))

    def marshal(self):
        """TODO"""
        return {
            'indices': {},
            'documents': {},
        }
