from unittest import TestCase

from ffmddb.core.models.config import Configuration


class BaseTestCase(TestCase):

    @classmethod
    def setup_class(cls):
        cls.config = Configuration.from_object({
            'test_config': {
                'collections': [{'name': 'foo', 'path': 'bar'}],
                'indices': [{'name': 'foo_idx', 'from': ['foo', 'document:']}]
            }
        })


class ConfigurationModelTestCase(BaseTestCase):

    def test_pass(self):
        self.assertEqual(self.config.name, 'test_config')


class ConfigFromObjectTestCase(TestCase):

    def test_two_root_keys_fails(self):
        with self.assertRaises(Configuration.MalformedConfiguration) as ctx:
            Configuration.from_object({'bad': {}, 'wolf': {}})
        self.assertTrue(
            'config may only contain one root-level key' in str(ctx.exception))

    def test_missing_required_keys_fails(self):
        with self.assertRaises(Configuration.MalformedConfiguration) as ctx:
            Configuration.from_object({
                'config': {}
            })
        self.assertTrue(
            'config must contain `collections` and `indices`'
            in str(ctx.exception))
        with self.assertRaises(Configuration.MalformedConfiguration) as ctx:
            Configuration.from_object({
                'config': {
                    'collections': []
                }
            })
        self.assertTrue(
            'config must contain `collections` and `indices`'
            in str(ctx.exception))
        with self.assertRaises(Configuration.MalformedConfiguration) as ctx:
            Configuration.from_object({
                'config': {
                    'indices': []
                }
            })
        self.assertTrue(
            'config must contain `collections` and `indices`'
            in str(ctx.exception))

    def test_colls_indices_not_lists_fails(self):
        with self.assertRaises(Configuration.MalformedConfiguration) as ctx:
            Configuration.from_object({
                'config': {
                    'collections': 'bad-wolf',
                    'indices': []
                }
            })
        self.assertTrue(
            '`collections` must be a list' in str(ctx.exception))
        with self.assertRaises(Configuration.MalformedConfiguration) as ctx:
            Configuration.from_object({
                'config': {
                    'collections': [],
                    'indices': 'bad-wolf'
                }
            })
        self.assertTrue(
            '`indices` must be a list' in str(ctx.exception))

    def test_malformed_collection_fails(self):
        with self.assertRaises(Configuration.MalformedConfiguration) as ctx:
            Configuration.from_object({
                'config': {
                    'collections': [{'bad': 'wolf'}],
                    'indices': []
                }
            })
        self.assertTrue(
            'collection `name` and `path` are required' in str(ctx.exception))

    def test_malformed_index_fails(self):
        with self.assertRaises(Configuration.MalformedConfiguration) as ctx:
            Configuration.from_object({
                'config': {
                    'collections': [{'name': 'foo', 'path': 'bar'}],
                    'indices': [{'bad': 'wolf'}]
                }
            })
        self.assertTrue(
            'index `name` and `from` fields are required'
            in str(ctx.exception))

    def test_malformed_collectionfield_reference_fails(self):
        with self.assertRaises(Configuration.MalformedConfiguration) as ctx:
            Configuration.from_object({
                'config': {
                    'collections': [{'name': 'foo', 'path': 'bar'}],
                    'indices': [{'name': 'bad-wolf', 'from': ['bad', 'wolf']}]
                }
            })
        self.assertTrue(
            'indicies must specify a valid collection by name'
            in str(ctx.exception))
        with self.assertRaises(Configuration.MalformedConfiguration) as ctx:
            Configuration.from_object({
                'config': {
                    'collections': [{'name': 'foo', 'path': 'bar'}],
                    'indices': [{
                        'name': 'bad-wolf',
                        'from': ['foo', 'document:'],
                        'to': ['bad', 'wolf'],
                    }]
                }
            })
        self.assertTrue(
            'indicies must specify a valid collection by name'
            in str(ctx.exception))

    def test_empty_config_succeeds(self):
        config = Configuration.from_object({
            'config': {
                'collections': [],
                'indices': [],
            }
        })
        self.assertEqual(config.name, 'config')
        self.assertEqual(len(config.collections), 0)
        self.assertEqual(len(config.indices), 0)

    def test_just_collections_succeeds(self):
        config = Configuration.from_object({
            'config': {
                'collections': [{'name': 'foo', 'path': 'bar'}],
                'indices': [],
            }
        })
        self.assertEqual(config.name, 'config')
        self.assertTrue('foo' in config.collections)
        self.assertEqual(len(config.collections), 1)
        self.assertEqual(len(config.indices), 0)

    def test_full_config_succeeds(self):
        config = Configuration.from_object({
            'config': {
                'collections': [
                    {'name': 'foo', 'path': 'bar'},
                    {'name': 'baz', 'path': 'qux'}
                ],
                'indices': [
                    {
                        'name': 'foo_idx',
                        'from': ['foo', 'document:']
                    },
                    {
                        'name': 'foo_baz',
                        'from': ['foo', 'name:'],
                        'to': ['baz', 'metadata:foo.name'],
                    },
                ]
            }
        })
        self.assertEqual(config.name, 'config')
        self.assertTrue('foo' in config.collections)
        self.assertTrue('foo_idx' in config.indices)
