ImageButler
===========

Simple image server built on Flask.

Developed Python version: Python 3.6.

Installation
------------

Using pip

.. code-block:: bash

    pip install ImageButler

Configuration & Environment Variables
-------------------------------------

Create *image_butler.conf* referring following example:

.. code-block:: text

    SQLALCHEMY_DATABASE_URI = 'sqlite:////<path-to-your>/ImageButler.db'
    SERVER_NAME = 'image.local-domain:5000'
    REDISLITE_PATH = '<path-to-your>/ImageButler.rdb'
    REDISLITE_WORKER_PID = '<path-to-your>/workers.pid'

Export environment variables:

.. code-block:: bash

    export FLASK_APP=imagebutler
    export IMAGEBUTLER_CONFIGS=path/to/your/image_butler.conf

For others configuration please referring to documents of *Flask*,
*Flask-Login*, *Flask-SQLAlchemy*... (please check *requirements.txt*).

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

User management
---------------

.. code-block:: bash

    flask user create your@email.address
    flask user get your@email.address
    flask user change_pass your@email.address

Upload images
-------------

For example we use cURL to upload the image.

.. code-block:: bash

    curl -X PUT \
        http://image.local-domain:5000/api/v0/image \
        -H 'content-type: multipart/form-data' \
        -F 'file=@/path/to/your/image.png;type=image/png' \
        -F username=1a339c02-404a-4b66-9fbb-cb30fb417c14 \
        -F 'password=knwAAOfLBcnkWzGxo0G/ZUzq9ukLb+gf5H/1nmPr7BE+im03qZarW4TvwVepYmi/cg9dEw+N4HDfLqQRfXBSdNawy7YkOQgwOYiRRq3t2PSjYd+Pme4SrMWUE1BYW5rt' \
        -F 'description=Image #1'

We got the result:

.. code-block:: text

    {"return": {"success": {"path": "/serve/image/1/97583609772e46729c2646c6fbfdef51.jpg"}}}

You can go to http://image.local-domain:5000/serve/image/1/97583609772e46729c2646c6fbfdef51.jpg
to see your image.
