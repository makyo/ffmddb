import six

try:
    from unittest import (
        TestCase,
        mock,
    )
except ImportError:
    from unittest import TestCase
    import mock

from ffmddb.core.database import Database


class BaseTestCase(TestCase):

    @classmethod
    def setup_class(cls):
        cls.db = Database({})


class DatabaseModelTestCase(BaseTestCase):

    def test_pass(self):
        self.assertEqual(1 + 1, 2)


class GetDocumentsMethodTestCase(BaseTestCase):

    def test_pass(self):
        self.db.get_documents('collection', {'query': []})
        self.assertEqual(1 + 1, 2)


class UpdateDocumentMethodTestCase(BaseTestCase):

    def test_pass(self):
        self.db.update_document('document', 'field', 'value')
        self.assertEqual(1 + 1, 2)


class DeleteDocumentMethodTestCase(BaseTestCase):

    def test_pass(self):
        self.db.delete_document('document')
        self.assertEqual(1 + 1, 2)


class CreateDocumentMethodTestCase(BaseTestCase):

    def test_pass(self):
        self.db.create_document('document')
        self.assertEqual(1 + 1, 2)


class GetCollectionMethodTestCase(BaseTestCase):

    def test_pass(self):
        self.db.get_collection('collection')
        self.assertEqual(1 + 1, 2)


class DeleteCollectionMethodTestCase(BaseTestCase):

    def test_pass(self):
        self.db.delete_collection('collection')
        self.assertEqual(1 + 1, 2)


class CreateCollectionMethodTestCase(BaseTestCase):

    def test_pass(self):
        self.db.create_collection('name', 'path')
        self.assertEqual(1 + 1, 2)


class CloseMethodTestCase(BaseTestCase):

    def test_closes_config_no_file(self):
        open_name = 'ffmddb.core.database.open'
        if six.PY2:
            open_name = '__builtin__.open'
        m = mock.mock_open()
        with mock.patch(open_name, m):
            self.db.close()
        self.assertEqual(m.call_count, 0)

    def test_closes_config_with_file(self):
        open_name = 'ffmddb.core.database.open'
        if six.PY2:
            open_name = '__builtin__.open'
        config = """
        test_db:
            collections:
                - name: foo
                  path: bar
            indices: []
        """
        m = mock.mock_open(read_data=config)
        with mock.patch(open_name, m):
            db = Database.from_file("filename")
        m = mock.mock_open()
        with mock.patch(open_name, m):
            db.close()
        self.assertEqual(m.call_count, 1)


class DBFromFileTestCase(TestCase):

    def test_creates_db_from_config_file(self):
        open_name = 'ffmddb.core.database.open'
        if six.PY2:
            open_name = '__builtin__.open'
        config = """
        test_db:
            collections:
                - name: foo
                  path: bar
            indices: []
        """
        m = mock.mock_open(read_data=config)
        with mock.patch(open_name, m):
            db = Database.from_file("filename")
        self.assertNotEqual(db, None)


class DBFromStringTestCase(TestCase):

    def test_creates_db_from_config_string(self):
        config = """
        test_db:
            collections:
                - name: foo
                  path: bar
            indices: []
        """
        db = Database.from_string(config)
        self.assertNotEqual(db, None)
