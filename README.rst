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

    curl -X POST \
        http://image.local-domain:5000/api/v0/image \
            -F file=@/path/to/your/image.jpg \
            -F username=df40767b-66b9-4b73-954d-3c0477abbe57 \
            -F 'password=phJi29Y20icaFQr2hR13PmQxw/YE9r4UBvOS6KEugnQLEXz+70qi/NNZ+i2U/713eG/VIRfnIkyCNAC8Qy7c9LqFH1QUUBzKgFsukKUpekK5OT57jUoEM/Tr0mWPfKMT'

We got the result:

.. code-block:: text

    {"return": {"success": {"path": "/serve/image/1/97583609772e46729c2646c6fbfdef51.jpg"}}}

You can go to http://image.local-domain:5000/serve/image/1/97583609772e46729c2646c6fbfdef51.jpg
to see your image.
