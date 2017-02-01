ffmddb Configuration
====================

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
        fence: ['<!--', '-->']
