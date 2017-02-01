class Collection:
    """Stores a reference to a collection of documents"""

    def __init__(self, name, path):
        self.name = name
        self.path = path


class CollectionField:
    """Stores an abstract reference to a field which should exist on most/all
    documents in a collection, used for indexing
    """

    def __init__(self, collection, field):
        self.collection = collection
        self.field = field


class Document:
    """Stores a reference to a single document"""

    def __init__(self, collection, name, document_field, metadata):
        self.collection = collection
        self.name = name
        self.document_field = document_field
        self.metadata = metadata
