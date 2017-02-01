"""
Models, to ffmddb are any thing that maps from a string or file to a python
object.

For files, this includes:

* a :py:class:`document <ffmddb.core.models.document.Document>`, which maps to
  one of the files ffmddb knows about
* a folder acting as a :py:class:`collection
  <ffmddb.core.models.document.Collection>` of documents
* an :py:class:`index <ffmddb.core.models.index.Index>` file

For strings, this includes:

* a :py:class:`configuration <ffmddb.core.models.config.Configuration>` YAML
  blob (which may come from a file)
* a json :py:class:`query <ffmddb.core.models.query.Query>` against the
  database (which may be a python dict)
* a :py:class:`field <ffmddb.core.models.field.Field>` spec

"""
