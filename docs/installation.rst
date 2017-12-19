Installation
============

Installation
------------

Using pip

.. code-block:: bash

    pip install ImageButler

Checkout current source code at
`GitHub's repo <https://github.com/ViiSiX/ImageButler>`_.

Configuration
-------------

Create *image_butler.conf* referring following example:

.. code-block:: text

    SQLALCHEMY_DATABASE_URI = 'sqlite:////<path-to-your>/ImageButler.db'
    SERVER_NAME = 'image.local-domain:5000'
    REDISLITE_PATH = '<path-to-your>/ImageButler.rdb'
    REDISLITE_WORKER_PID = '<path-to-your>/workers.pid'

    IMAGEBUTLER_MAX_THUMBNAIL = 150, 150
    IMAGEBUTLER_API_IMAGES_LIMIT = 5
    IMAGEBUTLER_MAX_IMAGE_SIZE = '1M'

    IMAGEBUTLER_REDISLITE_CACHE = False

For others configuration please referring to documents of *Flask*,
*Flask-Login*, *Flask-SQLAlchemy*... (please check *requirements.txt*).

You need to export environment variables by the following step.

Environment Variables
---------------------

.. code-block:: bash

    export FLASK_APP=imagebutler
    export IMAGEBUTLER_CONFIGS=path/to/your/image_butler.conf

Database Init
-------------

.. code-block:: bash

    flask db init
    flask db migrate
    flask db upgrade

**Note:**
- For MySQL and MariaDB please don't create your database in
*utf8_bin* collate since it will break the application.
- Also for MySQL and MariaDB, after run the *migrate* command,
go and edit your migrations/versions/<some-hex>_.py

.. code-block:: python

    from sqlalchemy.dialects.mysql import LONGBLOB
    # ...
    # ... replace the old fileContent line with
    sa.Column('fileContent', LONGBLOB(), nullable=False),
    # ...

Run
---

.. code-block:: bash

    flask run
