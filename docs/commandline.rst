Command-line Interface
======================

Before using command-line interface make sure you did set up
`the environment variables <installation.html#environment-variables>`_.

Users management
----------------

You can create new user, get user info or request the server to generate
a new password for your user. Users are identified by email address.

.. code-block:: bash

   flask user create your@email.address
   flask user get your@email.address
   flask user change_pass your@email.address

Images management
-----------------

Images management commands will help you to perform changes on multiple images.
For example: generate all images' thumbnail.

Generate images' thumbnail
^^^^^^^^^^^^^^^^^^^^^^^^^^

Generate images' thumbnail in bundle. There are two options for choosing:
all and missing (images which have not had thumbnail yet) .

.. code-block:: bash

   flask image gen_thumbnail --type all
   flask image gen_thumbnail --type missing
