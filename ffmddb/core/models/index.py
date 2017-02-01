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


class CrossCollectionIndex(Index):
    """Represents an index on one field common to a collection which maps to a
    field on another (or the same) collection.
    """

    def __init__(self, name, from_collection_field, to_collection_field):
        self.name = name
        self.from_collection_field = from_collection_field
        self.to_collection_field = to_collection_field
