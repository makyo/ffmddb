The ffmddb Database
===================

Documents and indices
---------------------

File format
-----------

Files which will be documents in the database should be textual. They can be of any format, so long as, when read, the fenced metadata may be found. For example, you could have a markdown file with a metadata block:

.. code-block:: markdown

    ---
    layout: post
    title: My great document
    tags:
        - foxes
        - cats
        - dogs
    ---

    Wow, foxes and dogs and cats are all *really great*!

In this instance, you can see that the file itself is an actual Jekyll file.

Fences do not need to be Jekyll style (three or more hyphens), but may be anything, so long as they're specified in the `configuration file <configuration.html>`__. For example, you can specify the fence to be an XML comment if you're storing XML-based documents.

In the configuration file:

.. code-block:: yaml

    mydb:
        ...
        fence: ['<!--ffmddb', '-->']

And in the document:

.. code-block:: xml

    <mydoc>
        <!--ffmddb
        foo: bar
        baz: qux
        -->
        ...
    </mydoc>
