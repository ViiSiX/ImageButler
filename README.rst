ImageButler
===========

Simple image server built on Flask.

Installation
------------

Using pip

.. code-block:: bash

    pip install Flask-Redislite

Configuration & Environment Variables
-------------------------------------

Create *image_butler.conf* referring following example:

.. code-block:: text

    SQLALCHEMY_DATABASE_URI = 'sqlite:////<path-to-your>/ImageButler.db'
    SERVER_NAME = 'image.local-domain:5000'
    REDISLITE_PATH = ''<path-to-your>/ImageButler.rdb'
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
