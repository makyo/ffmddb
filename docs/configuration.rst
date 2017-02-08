ffmddb Configuration
====================

``ffmddb`` relies on a single configuration file to figure out how to interact with the database. This file contains a YAML blob, which describes a few things about the structure of the data. It informs the database of where

Configuration file (.ffmddbrc) example:

.. code-block:: yaml
    :linenos:

    my_log_files:
        version: 1
        collections:
            - name: logs
              path: ./logs
            - name: participants
              path: ./participants
        indices:
            - name: log_tag
              from: ['logs', 'metadata:tag']
            - name: participants_logs
              from: ['participants', 'name:']
              to: ['logs', 'metadata:participants']
        fence: ['<!--ffmddb', '-->']

============  ========  ===========
Config entry  Default   Explanation
============  ========  ===========
|t1r1c1|      N/A       |t1r1c3|
|t1r2c1|      N/A       |t1r2c3|
|t1r3c1|      N/A       |t1r3c3|
|t1r4c1|      |t1r4c2|  |t1r4c3|
|t1r6c1|      |t1r6c2|  |t1r6c3|
|t1r7c1|      |t1r7c2|  |t1r7c3|
============  ========  ===========

some more

.. |t1r1c1| replace:: <Root level key>

.. |t1r1c3| replace:: The name of the database.

.. |t1r2c1| replace:: ``collections``

.. |t1r2c3| replace:: A list of YAML objects. Each object should containa ``name`` and a ``path`` entry. The ``name`` should contain letters, numbers, and underscores and start with a letter. The ``path`` should be relative to the configuration file. Can be empty.

.. |t1r3c1| replace:: ``indices``

.. |t1r3c3| replace:: A list of YAML objects. Each object should contain a name, a from field, and an optional to field. The name should contain letters, numbers, and underscores and start with a letter. The from and to fields should contain an array with the first item being the name of a collection and the second being a query for selecting one field. Can be empty, cannot contain data if ``collections`` is empty.

.. |t1r4c1| replace:: ``fence``

.. |t1r4c2| replace:: ``['---+', '---+']``

.. |t1r4c3| replace:: The fence that delineates the metadata field from the document field. Should be a two-item array, with the two items being strings containing the open fence and the close fence. The strings will be interpreted as regular expressions (the default being an example, specifying both fences as three or more hyphens), so be careful to escape where needed. fences occur on a line by themselves. Multiple metadata blocks may occur in a file; they will be merged before parsing.

.. |t1r6c1| replace:: ``index_path``

.. |t1r6c2| replace:: ``.ffmddb_idx``

.. |t1r6c3| replace:: The folder relative to the configuration file which contains the indices.

.. |t1r7c1| replace:: ``multiple_metadata``

.. |t1r7c2| replace:: False

.. |t1r7c3| replace:: Whether or not to collect metadata from multiple fenced blocks.
