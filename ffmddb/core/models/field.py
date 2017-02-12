FIELD_TYPES = (
    'document', 'd',
    'metadata', 'm',
    'name',     'n',
)

PATH_FIELDS = (
    'metadata', 'm',
)


class Field:

    def __init__(self, field_spec):
        """TODO"""
        self.field_spec = field_spec
        self.field_type, parts = Field.parse_spec(field_spec)
        if self.field_type in PATH_FIELDS:
            self.path_parts = parts
        else:
            self.path_parts = None

    def marshal(self):
        """TODO"""
        return self.field_spec

    def get(self, document):
        """TODO"""
        if self.field_type == 'd':
            return document._document_field
        elif self.field_type == 'n':
            return document._name
        elif self.field_type == 'm':
            result = document._metadata
            for part in self.path_parts:
                result = result.get(part, {})
            if result == {}:
                return None
            return result

    def set(self, document, value):
        """TODO"""
        if self.field_type == 'd':
            document._document_field = value
        elif self.field_type == 'n':
            document._name = value
        elif self.field_type == 'm':
            ultimate = self.path_parts[-1]
            result = document._metadata
            for part in self.path_parts[:-1]:
                result = result.get(part, {})
            result[ultimate] = value

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return str(self) == str(other)

    @classmethod
    def parse_spec(cls, spec):
        """TODO"""
        try:
            field_type, field_path = spec.split(':')
        except ValueError:
            raise cls.MalformedSpec(
                'spec must take the form of `type:path`; if `type` is '
                '"metadata", then `path` must be specified')
        if field_type not in FIELD_TYPES:
            raise cls.MalformedSpec(
                'valid field types are "document" and "metadata"')
        if field_type not in PATH_FIELDS and field_path != '':
            raise cls.MalformedSpec(
                'spec for the field type of {} must not contain a path'.format(
                    field_type))
        if field_type in PATH_FIELDS and field_path == '':
            raise cls.MalformedSpec(
                'spec for the field type of {} must contain a path'.format(
                    field_type))
        return field_type[0], field_path.split('.')

    class MalformedSpec(Exception):
        """TODO"""
        pass
