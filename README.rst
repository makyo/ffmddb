ffmddb
======

A flat-file-with-metadata database.

.. image:: https://travis-ci.org/makyo/ffmddb.svg?branch=master
    :target: https://travis-ci.org/makyo/ffmddb
.. image:: https://coveralls.io/repos/github/makyo/ffmddb/badge.svg?branch=master
    :target: https://coveralls.io/github/makyo/ffmddb?branch=master
.. image:: https://readthedocs.org/projects/ffmddb/badge/?version=latest
    :target: http://ffmddb.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status


This is a reference implementation for a simple document database idea based on flat-files, each of which contains at least one field (a large text blob, the document field) and potentially many other fields formed of structured data contained in a metadata blob within the file.

In short, it turns files written in a Jekyll fashion into objects in a database. The 'post content' turns into the document field, and the metadata blob turns into other fields. Indices are built and querying becomes possible within the indices (full document querying should rely on something like elasticsearch). The same data and relations are represented, but in a format easily edited in any text editor, easily readible or served from something like Jekyll, and easily stored in a VCS repo. The goal is not speed, but flexibility for manually interfacing with smaller datasets.
