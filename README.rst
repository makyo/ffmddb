ffmddb
======

A flat-file-with-metadata database.

This is a reference implementation for a simple document database idea based on flat-files, each of which contains at least one field (a large text blob, the document field) and potentially many other fields formed of structured data contained in a metadata blob within the file.

In short, it turns files written in a Jekyll fashion into objects in a database. The 'post content' turns into the document field, and the metadata blob turns into other fields. Indices are built and querying becomes possible within the indices (full document querying should rely on something like elasticsearch).