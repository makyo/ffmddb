from unittest import TestCase

from ffmddb.core.database import Database
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
        d = Document(Collection('name', 'path'), 'name', 'asdf', {})
        d.marshal()
        self.assertEqual(1 + 1, 2)


class ReadDocumentTestCase(TestCase):

    @classmethod
    def setUp(cls):
        config = """
        test_db:
            collections:
                - name: foo
                  path: ''
            indices: []
        """
        cls.db = Database.from_string(config)
        cls.doc1 = Document(cls.db,
                            cls.db.config.collections['foo'],
                            'ffmddb/core/models/fixtures/document.txt')
        cls.doc2 = Document(cls.db,
                            cls.db.config.collections['foo'],
                            'ffmddb/core/models/fixtures/document-malformed'
                            '.txt')
        cls.doc3 = Document(cls.db,
                            cls.db.config.collections['foo'],
                            'ffmddb/core/models/fixtures/document-fenced.txt')

    def test_defaults(self):
        self.doc1._read()
        self.assertEqual(self.doc1.document_field.strip(), 'Document data')
        self.assertEqual(self.doc1.metadata, {
            'foo': {
                'bar': 42,
            },
            'qux': ['a', 'b', 'c'],
        })
        self.assertTrue(self.doc1.valid)

    def test_no_metadata_invalid(self):
        self.doc2._read()
        self.assertFalse(self.doc2.valid)

    def test_non_default_fence(self):
        self.db.config.options['fence'] = ['<!--', '-->']
        self.doc3._read()
        self.assertEqual(
            self.doc3.document_field.strip(),
            'Document data\n\n<!--\nadditional: metadata\n-->')
        self.assertEqual(self.doc3.metadata, {
            'foo': {
                'bar': 42,
            },
            'qux': ['a', 'b', 'c'],
        })
        self.assertTrue(self.doc3.valid)

    def test_multiple_metadata(self):
        self.db.config.options['fence'] = ['<!--', '-->']
        self.db.config.options['multiple_metadata'] = True
        self.doc3._read()
        self.assertEqual(self.doc3.document_field.strip(), 'Document data')
        self.assertEqual(self.doc3.metadata, {
            'foo': {
                'bar': 42,
            },
            'qux': ['a', 'b', 'c'],
            'additional': 'metadata',
        })
        self.assertTrue(self.doc3.valid)
