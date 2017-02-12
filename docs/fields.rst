Fields
======

Fields provide a way to point to a specific portion of a document, whether it's the document field, the name of the document or a portion of the metadata. In most cases, this takes the form of a 'field spec', which is a string describing what kind and where the field is.

There are three field types:

Name
  The name field refers to the document's name, usually its filename. It's specified with ``name`` or ``n``.
Document
  The document field is the contents of the document itself, not including the metadata. It's specified with ``document`` or ``d``.
Metadata
  The metadata field refers to some portion of the metadata which is described by the path portion of the field spec. It's specified with ``metadata`` or ``m``

The field spec takes the form ``type:path``, with path only being allowed for metadata types (but the colon being required always). For instance, if you want to to reference the document's name, you can use a field spec of ``n:`` or ``name:``. Similarly, referencing the document field would have a spec of ``d:`` or ``document:``.

For metadata fields, you can write the object's location in the yaml tree through dot notation. Given this metadata::

    foo:
        bar: baz
    qux:
        - 1
        - 2

You could reference the bar field with the field spec ``m:foo.bar`` or ``metadata:foo.bar``.

Passing a field spec to the field class's constructor will build an object from that field which contains a few helpful methods. A field object has both :py:func:`get <ffmddb.core.models.field.Field.get>` and :py:func:`set <ffmddb.core.models.field.Field.set>` methods. Passing a document to the object's ``get`` method will return the matching field, while passing a document and a value to the ``set`` method will set that field on the document to the provided value.

Generally, however, these methods are not called directly. The :py:func:`update <ffmddb.core.models.document.Document.update>` accepts a field and a value and performs the work of calling ``set`` for you, while also marking the resulting document as dirty, meaning that it will need to be committed (written to disk). The ``get`` method is called by `querying <queries.html>`__.
