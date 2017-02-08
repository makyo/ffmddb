from unittest import TestCase

from ffmddb.core.models.document import Document
from ffmddb.core.models.field import Field


class FieldModelTestCase(TestCase):

    def test_populates_fields(self):
        field = Field('document:')
        self.assertEqual(field.field_type, 'document')
        self.assertEqual(field.path_parts, None)
        field = Field('metadata:foo.bar')
        self.assertEqual(field.field_type, 'metadata')
        self.assertEqual(field.path_parts, ['foo', 'bar'])


class MarshalTestCase(TestCase):

    def test_marshal(self):
        field = Field('document:')
        self.assertEqual(field.marshal(), 'document:')


class RunTestCase(TestCase):

    @classmethod
    def setup_class(cls):
        cls.d = Document(db={},
                         collection='collection',
                         name='Test document',
                         document_field="asdf",
                         metadata={
                             'foo': {
                                 'bar': 42,
                             },
                             'qux': ['a', 'b', 'c']
                         })

    def test_document(self):
        field = Field('document:')
        self.assertEqual(field.run(self.d), 'asdf')

    def test_name(self):
        field = Field('name:')
        self.assertEqual(field.run(self.d), 'Test document')

    def test_metadata(self):
        field = Field('metadata:foo.bar')
        self.assertEqual(field.run(self.d), 42)
        field = Field('metadata:foo.baz')
        self.assertEqual(field.run(self.d), None)


class ParseSpecTestCase(TestCase):

    def test_document_field(self):
        spec = Field.parse_spec('document:')
        self.assertEqual(spec[0], 'document')
        self.assertEqual(spec[1], [''])

    def test_metadata_field(self):
        spec = Field.parse_spec('metadata:foo')
        self.assertEqual(spec[0], 'metadata')
        self.assertEqual(spec[1], ['foo'])
        spec = Field.parse_spec('metadata:foo.bar')
        self.assertEqual(spec[0], 'metadata')
        self.assertEqual(spec[1], ['foo', 'bar'])

    def test_field_type_required(self):
        with self.assertRaises(Field.MalformedSpec) as context:
            Field.parse_spec('document...')
        print(dir(context.exception))
        self.assertTrue(
            'spec must take the form of `type:path`' in str(context.exception))

    def test_invalid_field_type(self):
        with self.assertRaises(Field.MalformedSpec) as context:
            Field.parse_spec('bad-wolf:')
        self.assertTrue(
            'valid field types are "document" and "metadata"' in
            str(context.exception))

    def test_document_with_path_invalid(self):
        with self.assertRaises(Field.MalformedSpec) as context:
            Field.parse_spec('document:bad-wolf')
        self.assertTrue(
            'document must not contain a path' in str(context.exception))

    def test_metadata_without_path_invalid(self):
        with self.assertRaises(Field.MalformedSpec) as context:
            Field.parse_spec('metadata:')
        self.assertTrue(
            'metadata must contain a path' in str(context.exception))
