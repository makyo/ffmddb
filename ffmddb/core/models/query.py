class Filter:
    """Stores a single filter for comparing a field to a value"""

    OPERATORS = (
        'eq',
        'ne',
        'gt',
        'lt',
        'in',
        'contains',
    )

    def __init__(self, filter_obj):
        """creates a filter object from a dict"""
        self.field = filter_obj['field']
        self.operator = filter_obj['op']
        self.value = filter_obj['value']

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

    CONJUNCTIONS = (
        'and',
        'or',
        'not',
    )

    def __init__(self, conjunction, filter_list):
        """creates a filter group object from a conjunction and list of filters
        """
        self.conjunction = conjunction
        self.filter_list = filter_list

    @classmethod
    def is_filter_group(cls, obj):
        """duck-types a dict to see if it looks like a filter-group"""
        try:
            if len(obj) != 1:
                return False
            if (list(obj.keys()))[0] not in cls.CONJUNCTIONS:
                return False
            if type((list(obj.values()))[0]) not in [list, tuple]:
                return False
            return True
        except:
            return False


class Query:
    """Stores an arbitrarily complex query"""

    def __init__(self, query_obj):
        """creates a query from a dict"""
        self.core_group = self._parse_group('and', query_obj['query'])

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
