from unittest import TestCase

from ffmddb.core.models.document import Document
from ffmddb.core.models.field import Field
from ffmddb.core.models.query import (
    Filter,
    FilterGroup,
    Query,
)


class FilterModelTestCase(TestCase):

    def test_create(self):
        f = Filter({'field': 'd:', 'op': 'eq', 'value': 'asdf'})
        self.assertEqual(f.field, Field('d:'))
        self.assertEqual(f.operator, 'eq')
        self.assertEqual(f.value, 'asdf')


class RunFilterTestCase(TestCase):

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

    def test_eq(self):
        f = Filter({'field': 'd:', 'op': 'eq', 'value': 'asdf'})
        self.assertTrue(f.run(self.d))
        f = Filter({'field': 'd:', 'op': 'eq', 'value': 'bad-wolf'})
        self.assertFalse(f.run(self.d))

    def test_ne(self):
        f = Filter({'field': 'd:', 'op': 'ne', 'value': '42'})
        self.assertTrue(f.run(self.d))
        f = Filter({'field': 'd:', 'op': 'ne', 'value': 'asdf'})
        self.assertFalse(f.run(self.d))

    def test_gt(self):
        f = Filter({'field': 'm:foo.bar', 'op': 'gt', 'value': 40})
        self.assertTrue(f.run(self.d))
        f = Filter({'field': 'm:foo.bar', 'op': 'gt', 'value': 45})
        self.assertFalse(f.run(self.d))

    def test_lt(self):
        f = Filter({'field': 'm:foo.bar', 'op': 'lt', 'value': 45})
        self.assertTrue(f.run(self.d))
        f = Filter({'field': 'm:foo.bar', 'op': 'lt', 'value': 40})
        self.assertFalse(f.run(self.d))

    def test_ge(self):
        f = Filter({'field': 'm:foo.bar', 'op': 'ge', 'value': 40})
        self.assertTrue(f.run(self.d))
        f = Filter({'field': 'm:foo.bar', 'op': 'ge', 'value': 42})
        self.assertTrue(f.run(self.d))
        f = Filter({'field': 'm:foo.bar', 'op': 'ge', 'value': 45})
        self.assertFalse(f.run(self.d))

    def test_le(self):
        f = Filter({'field': 'm:foo.bar', 'op': 'le', 'value': 45})
        self.assertTrue(f.run(self.d))
        f = Filter({'field': 'm:foo.bar', 'op': 'le', 'value': 42})
        self.assertTrue(f.run(self.d))
        f = Filter({'field': 'm:foo.bar', 'op': 'le', 'value': 40})
        self.assertFalse(f.run(self.d))

    def test_in(self):
        f = Filter({'field': 'm:foo.bar', 'op': 'in', 'value': [42]})
        self.assertTrue(f.run(self.d))
        f = Filter({'field': 'm:foo.bar', 'op': 'in', 'value': [41]})
        self.assertFalse(f.run(self.d))

    def test_contains(self):
        f = Filter({'field': 'm:qux', 'op': 'contains', 'value': 'a'})
        self.assertTrue(f.run(self.d))
        f = Filter({'field': 'm:qux', 'op': 'contains', 'value': 'z'})
        self.assertFalse(f.run(self.d))


class FilterIsFilterTestCase(TestCase):

    def test_is_filter_bad_keys_fails(self):
        self.assertFalse(Filter.is_filter(
            {'bad': 'wolf'}))

    def test_is_filter_bad_op_fails(self):
        self.assertFalse(Filter.is_filter(
            {'field': 'asdf', 'op': 'bad-wolf', 'value': 'qwer'}))

    def test_is_filter_exception_fails(self):
        self.assertFalse(Filter.is_filter('bad-wolf'))


class FilterGroupModelTestCase(TestCase):

    def test_create(self):
        f = FilterGroup('and', [])
        self.assertEqual(f.conjunction, 'and')
        self.assertEqual(f.filter_list, [])


class RunFilterGroupTestCase(TestCase):

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

    def test_and(self):
        f = FilterGroup(
            'and',
            [
                Filter({'field': 'd:', 'op': 'eq', 'value': 'asdf'}),
                Filter({'field': 'm:foo.bar', 'op': 'eq', 'value': 42}),
            ])
        self.assertTrue(f.run(self.d))
        f = FilterGroup(
            'and',
            [
                Filter({'field': 'd:', 'op': 'eq', 'value': 'bad-wolf'}),
                Filter({'field': 'm:foo.bar', 'op': 'eq', 'value': 42}),
            ])
        self.assertFalse(f.run(self.d))

    def test_or(self):
        f = FilterGroup(
            'or',
            [
                Filter({'field': 'd:', 'op': 'eq', 'value': 'asdf'}),
                Filter({'field': 'm:foo.bar', 'op': 'eq', 'value': 42}),
            ])
        self.assertTrue(f.run(self.d))
        f = FilterGroup(
            'or',
            [
                Filter({'field': 'd:', 'op': 'eq', 'value': 'bad-wolf'}),
                Filter({'field': 'm:foo.bar', 'op': 'eq', 'value': 42}),
            ])
        self.assertTrue(f.run(self.d))
        f = FilterGroup(
            'or',
            [
                Filter({'field': 'd:', 'op': 'eq', 'value': 'bad-wolf'}),
                Filter({'field': 'm:foo.bar', 'op': 'eq', 'value': 43}),
            ])
        self.assertFalse(f.run(self.d))

    def test_not(self):
        f = FilterGroup(
            'not',
            [
                Filter({'field': 'd:', 'op': 'eq', 'value': 'asdf'}),
                Filter({'field': 'm:foo.bar', 'op': 'eq', 'value': 42}),
            ])
        self.assertFalse(f.run(self.d))
        f = FilterGroup(
            'not',
            [
                Filter({'field': 'd:', 'op': 'eq', 'value': 'bad-wolf'}),
                Filter({'field': 'm:foo.bar', 'op': 'eq', 'value': 42}),
            ])
        self.assertTrue(f.run(self.d))


class FilterGroupIsFilterGroupTestCase(TestCase):

    def test_is_filter_group_bad_len_fails(self):
        self.assertFalse(FilterGroup.is_filter_group(
            {'or': [], 'and': []}))

    def test_is_filter_group_bad_conjunction_fails(self):
        self.assertFalse(FilterGroup.is_filter_group(
            {'bad-wolf': []}))

    def test_is_filter_group_bad_value_fails(self):
        self.assertFalse(FilterGroup.is_filter_group(
            {'or': 'bad-wolf'}))

    def test_is_filter_group_exception_fails(self):
        self.assertFalse(FilterGroup.is_filter_group(['bad-wolf']))


class QueryModelTestCase(TestCase):

    def test_create(self):
        q = Query({'query': []})
        self.assertEqual(len(q.core_group.filter_list), 0)


class RunQueryTestCase(TestCase):

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

    def test_run(self):
        q = Query({'query': [
            {'field': 'n:', 'op': 'eq', 'value': 'Test document'},
            {'and': [
                {'field': 'd:', 'op': 'eq', 'value': 'asdf'},
                {'field': 'm:foo.bar', 'op': 'eq', 'value': 42},
            ]}
        ]})
        self.assertTrue(q.run(self.d))
        q = Query({'query': [
            {'field': 'n:', 'op': 'eq', 'value': 'Test document'},
            {'and': [
                {'field': 'd:', 'op': 'eq', 'value': 'bad-wolf'},
                {'field': 'm:foo.bar', 'op': 'eq', 'value': 42},
            ]}
        ]})
        self.assertFalse(q.run(self.d))


class QueryParseGroupTestCase(TestCase):

    def test_parse_group_filter(self):
        q = Query({'query': [
            {'field': 'name:', 'op': 'eq', 'value': 'foo'},
        ]})
        self.assertEqual(len(q.core_group.filter_list), 1)

    def test_parse_group_filter_group(self):
        q = Query({'query': [
            {'or': [
                {'field': 'name:', 'op': 'eq', 'value': 'foo'},
                {'field': 'name:', 'op': 'eq', 'value': 'bar'},
            ]},
        ]})
        self.assertEqual(len(q.core_group.filter_list), 1)

    def test_parse_group_complex(self):
        q = Query({'query': [
            {'field': 'm:type', 'op': 'ne', 'value': 'buzzword'},
            {'or': [
                {'field': 'name:', 'op': 'eq', 'value': 'foo'},
                {'field': 'name:', 'op': 'eq', 'value': 'bar'},
            ]},
        ]})
        self.assertEqual(len(q.core_group.filter_list), 2)

    def test_parse_group_bad_data(self):
        with self.assertRaises(Query.MalformedQuery) as ctx:
            Query({'query': ['asdf']})
        self.assertTrue(
            'item asdf does not appear to be a filter or filter'
            in str(ctx.exception))
