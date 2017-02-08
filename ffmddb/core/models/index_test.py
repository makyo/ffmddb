from unittest import TestCase

from ffmddb.core.models.document import (
    Collection,
    CollectionField,
)
from ffmddb.core.models.field import Field
from ffmddb.core.models.index import (
    Index,
    SingleCollectionIndex,
    CrossCollectionIndex,
)


class IndexModelTestCase(TestCase):

    @classmethod
    def setup_class(cls):
        cls.i = Index()

    def test_pass(self):
        self.i.read()
        self.i.write()
        self.assertEqual(1 + 1, 2)


class SingleCollectionIndexModelTestCase(TestCase):

    @classmethod
    def setup_class(cls):
        collection_field = CollectionField(
            Collection('name', 'path'),
            Field('document:'))
        cls.i = SingleCollectionIndex("name", collection_field)

    def test_pass(self):
        self.assertEqual(1 + 1, 2)


class MarshalSingleCollectionIndexTestCase(TestCase):

    @classmethod
    def setup_class(cls):
        collection_field = CollectionField(
            Collection('name', 'path'),
            Field('document:'))
        cls.i = SingleCollectionIndex("name", collection_field)

    def test_marshal(self):
        self.assertEqual(self.i.marshal(), {
            'name': 'name',
            'from': ['name', 'document:'],
        })


class CrossCollectionIndexModelTestCase(TestCase):

    @classmethod
    def setup_class(cls):
        from_collection_field = CollectionField(
            Collection('from', 'path'),
            Field('document:'))
        to_collection_field = CollectionField(
            Collection('to', 'path'),
            Field('document:'))
        cls.i = CrossCollectionIndex(
            "name", from_collection_field, to_collection_field)

    def test_pass(self):
        self.assertEqual(1 + 1, 2)


class MarshalCrossCollectionIndexTestCase(TestCase):

    @classmethod
    def setup_class(cls):
        from_collection_field = CollectionField(
            Collection('from', 'path'),
            Field('document:'))
        to_collection_field = CollectionField(
            Collection('to', 'path'),
            Field('document:'))
        cls.i = CrossCollectionIndex(
            "name", from_collection_field, to_collection_field)

    def test_marshal(self):
        self.assertEqual(self.i.marshal(), {
            'name': 'name',
            'from': ['from', 'document:'],
            'to': ['to', 'document:'],
        })
