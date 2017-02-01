from unittest import TestCase

from ffmddb.core.models.query import (
    Filter,
    FilterGroup,
    Query,
)


class FilterModelTestCase(TestCase):

    def test_create(self):
        f = Filter({'field': 'document:', 'op': 'eq', 'value': 'asdf'})
        self.assertEqual(f.field, 'document:')
        self.assertEqual(f.operator, 'eq')
        self.assertEqual(f.value, 'asdf')

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
            {'field': 'metadata:type', 'op': 'ne', 'value': 'buzzword'},
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
