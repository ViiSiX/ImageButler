ImageButler
===========

Simple image server built on Flask.

Developed Python version: Python 3.6.

.. image:: https://travis-ci.org/ViiSiX/ImageButler.svg?branch=R%2F0.0
    :target: https://travis-ci.org/ViiSiX/ImageButler

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

    IMAGEBUTLER_MAX_THUMBNAIL = 150, 150
    IMAGEBUTLER_API_IMAGES_LIMIT = 5
    IMAGEBUTLER_MAX_IMAGE_SIZE = '1M'

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

Upload image
------------

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

    {
        "return": {
            "success": {
                "file_name": "ca4ffe9f192f4f358e4981ceaafd8068.jpg",
                "path": "/serve/image/1/ca4ffe9f192f4f358e4981ceaafd8068.jpg",
                "thumbnail": "/serve/thumbnail/1/ca4ffe9f192f4f358e4981ceaafd8068.jpg",
                "description": "Dog's Image"
            }
        }
    }

You can go to http://image.local-domain:5000/serve/image/1/ca4ffe9f192f4f358e4981ceaafd8068.jpg
to see your image.

Update your image's description
-------------------------------

.. code-block:: bash

    curl -X POST \
          http://image.local-domain:5000/api/v0/image \
          -H 'content-type: application/json' \
          -d '{
            "username": "1a339c02-404a-4b66-9fbb-cb30fb417c14",
            "password": "knwAAOfLBcnkWzGxo0G/ZUzq9ukLb+gf5H/1nmPr7BE+im03qZarW4TvwVepYmi/cg9dEw+N4HDfLqQRfXBSdNawy7YkOQgwOYiRRq3t2PSjYd+Pme4SrMWUE1BYW5rt",
            "filename": "ca4ffe9f192f4f358e4981ceaafd8068.jpg",
            "description": "Cat's image"
        }'

Then we got the similar result of create new image:

.. code-block:: text

    {
        "return": {
            "success": {
                "file_name": "ca4ffe9f192f4f358e4981ceaafd8068.jpg",
                "path": "/serve/image/1/ca4ffe9f192f4f358e4981ceaafd8068.jpg",
                "thumbnail": "/serve/thumbnail/1/ca4ffe9f192f4f358e4981ceaafd8068.jpg",
                "description": "Cat's Image"
            }
        }
    }

Delete an image
---------------

.. code-block:: bash

    curl -X DELETE \
          http://image.local-domain:5000/api/v0/image \
          -H 'content-type: application/json' \
          -d '{
            "username": "1a339c02-404a-4b66-9fbb-cb30fb417c14",
            "password": "knwAAOfLBcnkWzGxo0G/ZUzq9ukLb+gf5H/1nmPr7BE+im03qZarW4TvwVepYmi/cg9dEw+N4HDfLqQRfXBSdNawy7YkOQgwOYiRRq3t2PSjYd+Pme4SrMWUE1BYW5rt",
            "filename": "ca4ffe9f192f4f358e4981ceaafd8068.jpg",
        }'

Get your images
---------------

.. code-block:: bash

    curl -X POST \
        http://image.local-domain:5000/api/v0/images \
        -H 'content-type: application/json' \
        -d {
            "username": "1a339c02-404a-4b66-9fbb-cb30fb417c14",
            "password": "knwAAOfLBcnkWzGxo0G/ZUzq9ukLb+gf5H/1nmPr7BE+im03qZarW4TvwVepYmi/cg9dEw+N4HDfLqQRfXBSdNawy7YkOQgwOYiRRq3t2PSjYd+Pme4SrMWUE1BYW5rt",
            "page": 1
        }
