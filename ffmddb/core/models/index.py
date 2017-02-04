class Index:
    """Provides an interface of common methods for collection types"""

    def read(self):
        pass

    def write(self):
        pass


class SingleCollectionIndex(Index):
    """Represents an index on one field common to a collection"""

    def __init__(self, name, collection_field):
        self.name = name
        self.collection_field = collection_field

    def marshal(self):
        return {
            'name': self.name,
            'from': self.collection_field.marshal(),
        }


class CrossCollectionIndex(Index):
    """Represents an index on one field common to a collection which maps to a
    field on another (or the same) collection
    """

    def __init__(self, name, from_collection_field, to_collection_field):
        self.name = name
        self.from_collection_field = from_collection_field
        self.to_collection_field = to_collection_field

    def marshal(self):
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
        self.indices = {}
        self.documents = {}
