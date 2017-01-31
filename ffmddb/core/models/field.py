class Field:

    def __init__(self, field_spec):
        self.field_type, parts = Field.parse_spec(field_spec)
        if self.field_type == 'document':
            self.path_parts = []
        else:
            self.path_parts = parts

    @classmethod
    def parse_spec(cls, spec):
        try:
            field_type, field_path = spec.split(':')
        except ValueError:
            raise Field.MalformedSpec(
                'spec must take the form of `type:path`; if `type` is '
                '"document", then `path` must be empty')
        if field_type not in ['document', 'metadata']:
            raise Field.MalformedSpec(
                'valid field types are "document" and "metadata"')
        if field_type == 'document' and field_path != '':
            raise Field.MalformedSpec(
                'spec for the field type of document must not contain a path')
        if field_type == 'metadata' and field_path == '':
            raise Field.MalformedSpec(
                'spec for the field type of metadata must contain a path')
        return field_type, field_path.split('.')

    class MalformedSpec(Exception):
        pass
