from unittest import TestCase

from ffmddb.core.models.document import (
    Collection,
    CollectionField,
    Document,
)
from ffmddb.core.models.field import Field


class CollectionModelTestCase(TestCase):

    def test_pass(self):
        Collection('name', 'path')
        self.assertEqual(1 + 1, 2)


class CollectionFieldModelTestCase(TestCase):

    def test_pass(self):
        CollectionField(
            Collection('name', 'path'),
            Field('document:'))
        self.assertEqual(1 + 1, 2)


class DocumentModelTestCase(TestCase):

    def test_pass(self):
        Document(Collection('name', 'path'), 'name', 'asdf', {})
        self.assertEqual(1 + 1, 2)
