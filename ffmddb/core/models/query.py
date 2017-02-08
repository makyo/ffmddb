from functools import reduce

from ffmddb.core.models.field import Field


class Filter:
    """Stores a single filter for comparing a field to a value"""

    #: OPERATORS contains a list of comparisons and operations for running
    #: queries
    OPERATORS = {
        'eq': lambda x, y: x == y,
        'ne': lambda x, y: x != y,
        'gt': lambda x, y: x > y,
        'lt': lambda x, y: x < y,
        'ge': lambda x, y: x >= y,
        'le': lambda x, y: x <= y,
        'in': lambda x, y: x in y,
        'contains': lambda x, y: y in x,
    }

    def __init__(self, filter_obj):
        """creates a filter object from a dict"""
        self.field = Field(filter_obj['field'])
        self.operator = filter_obj['op']
        self.value = filter_obj['value']

    def run(self, document):
        """runs the test against the document, comparing the metadata field
        specified by the filter's field against the provided value using the
        provided operation
        """
        return self.OPERATORS[self.operator](
            self.field.run(document),
            self.value)

    @classmethod
    def is_filter(cls, obj):
        """duck-types a dict to see if it looks like a filter object"""
        try:
            if sorted(obj.keys()) != ['field', 'op', 'value']:
                return False
            if obj['op'] not in cls.OPERATORS:
                return False
            return True
        except:
            return False


class FilterGroup:
    """Stores a list of filter objects joined by a conjunction"""

    CONJUNCTIONS = {
        'and': lambda l: reduce(lambda memo, item: memo and item, l),
        'or': lambda l: reduce(lambda memo, item: memo or item, l),
        'not': lambda l: not reduce(lambda memo, item: memo and item, l),
    }

    def __init__(self, conjunction, filter_list):
        """creates a filter group object from a conjunction and list of filters
        """
        self.conjunction = conjunction
        self.filter_list = filter_list

    def run(self, document):
        """runs each specified filter in the group and reduces the results to a
        single value with the provided conjunction
        """
        result = [filter_or_group.run(document) for filter_or_group
                  in self.filter_list]
        return self.CONJUNCTIONS[self.conjunction](result)

    @classmethod
    def is_filter_group(cls, obj):
        """duck-types a dict to see if it looks like a filter-group"""
        try:
            o = obj.copy()
            if len(o) != 1:
                return False
            k, v = o.popitem()
            if k not in cls.CONJUNCTIONS:
                return False
            if type(v) not in [list, tuple]:
                return False
            return True
        except:
            return False


class Query:
    """Stores an arbitrarily complex query"""

    def __init__(self, query_obj):
        """creates a query from a dict"""
        self.core_group = self._parse_group('and', query_obj['query'])

    def run(self, document):
        """runs the core filter group which contains all filters and groups in
        the query
        """
        return self.core_group.run(document)

    def _parse_group(self, conjunction, query_list):
        """parses a single entry in the query dict either as a filter or filter
        group
        """
        group_items = []
        for item in query_list:
            if Filter.is_filter(item):
                group_items.append(Filter(item))
            elif FilterGroup.is_filter_group(item):
                item_conjunction, item_list = item.popitem()
                group_items.append(self._parse_group(
                    item_conjunction, item_list))
            else:
                raise Query.MalformedQuery(
                    'item {} does not appear to be a filter or filter '
                    'group'.format(item))
        return FilterGroup(conjunction, group_items)

    class MalformedQuery(Exception):
        pass
