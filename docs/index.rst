.. ffmddb documentation master file, created by
   sphinx-quickstart on Wed Feb  1 11:47:50 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

ffmddb Documentation
====================

A flat-file-with-metadata database.

.. image:: https://travis-ci.org/makyo/ffmddb.svg?branch=master
    :target: https://travis-ci.org/makyo/ffmddb
.. image:: https://coveralls.io/repos/github/makyo/ffmddb/badge.svg?branch=master
    :target: https://coveralls.io/github/makyo/ffmddb?branch=master


This is a reference implementation for a simple document database idea based on flat-files, each of which contains at least one field (a large text blob, the document field) and potentially many other fields formed of structured data contained in a metadata blob within the file.

In short, it turns files written in a Jekyll fashion into objects in a database. The 'post content' turns into the document field, and the metadata blob turns into other fields. Indices are built and querying becomes possible within the indices (full document querying should rely on something like elasticsearch).

.. toctree::
   :maxdepth: 1
   :caption: Contents:

   usage
   API <api/index>
   use-case
