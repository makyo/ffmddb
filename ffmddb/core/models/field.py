FIELD_TYPES = (
    'document',
    'metadata',
    'name',
)

PATH_FIELDS = (
    'metadata',
)


class Field:

    def __init__(self, field_spec):
        self.field_type, parts = Field.parse_spec(field_spec)
        if self.field_type in PATH_FIELDS:
            self.path_parts = parts
        else:
            self.path_parts = None

    @classmethod
    def parse_spec(cls, spec):
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
        return field_type, field_path.split('.')

    class MalformedSpec(Exception):
        pass
