from unittest import TestCase

from .field import Field


class FieldModel_init_TestCase(TestCase):

    def test_populates_fields(self):
        field = Field('document:')
        self.assertEqual(field.field_type, 'document')
        self.assertEqual(field.path_parts, [])
        field = Field('metadata:foo.bar')
        self.assertEqual(field.field_type, 'metadata')
        self.assertEqual(field.path_parts, ['foo', 'bar'])


class FieldModel_parse_spec_TestCase(TestCase):

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
