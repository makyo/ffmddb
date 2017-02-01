ffmddb
======

A flat-file-with-metadata database.

.. image:: https://travis-ci.org/makyo/ffmddb.svg?branch=master
    :target: https://travis-ci.org/makyo/ffmddb
.. image:: https://coveralls.io/repos/github/makyo/ffmddb/badge.svg?branch=master
    :target: https://coveralls.io/github/makyo/ffmddb?branch=master


This is a reference implementation for a simple document database idea based on flat-files, each of which contains at least one field (a large text blob, the document field) and potentially many other fields formed of structured data contained in a metadata blob within the file.

In short, it turns files written in a Jekyll fashion into objects in a database. The 'post content' turns into the document field, and the metadata blob turns into other fields. Indices are built and querying becomes possible within the indices (full document querying should rely on something like elasticsearch).

Rationale
---------

`ffmddb` was born from the idea that the best tool for editing a textfile is a text editor, and yet even text files benefit from managed metadata and relations between objects, as shown by a case study:

    I've been on the 'net for well over twenty years now, and over that period of time, I've amassed hundreds of log files. Some are notes, some are important conversations that led to relationship, some are inane conversations with individuals who have since passed away.

    In that time, I've run through several different organizational schemes, databases, and projects to manage these files. I wanted the organizational benefits of a relational database, the freedom of a document database, and the flexibility of editing the files by hand. Finally, I wanted the ability to keep the files in a repository.

For the above problem space, the relation solution would be:

* A table of participants (name, about)
* A table of logs (name, text, date)
* A mapping table (log, participant)

In `ffmddb`, that maps to:

* A folder of participant files, text files with any document data, named after the participant
* A folder of log files, text files with any document data, and metadata containing a list of participants and the date of the log
* An index file containing mapping between logs by participant for faster queries

The same data and relations are represented, but in a format easily edited in any text editor, easily readible or served from something like Jekyll, and easily stored in a VCS repo. The goal is not speed, but flexibility for manually interfacing with smaller datasets.
