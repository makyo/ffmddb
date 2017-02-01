from unittest import TestCase

from ffmddb.core.models.document import (
    Collection,
    CollectionField,
    Document,
)
from ffmddb.core.models.field import Field


class CollectionModel_Init_TestCase(TestCase):

    def test_pass(self):
        Collection('name', 'path')
        self.assertEqual(1 + 1, 2)


class CollectionFieldModel_Init_TestCase(TestCase):

    def test_pass(self):
        CollectionField(
            Collection('name', 'path'),
            Field('document:'))
        self.assertEqual(1 + 1, 2)


class DocumentModel_Init_TestCase(TestCase):

    def test_pass(self):
        Document(Collection('name', 'path'), 'name', 'asdf', {})
        self.assertEqual(1 + 1, 2)
