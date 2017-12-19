REST APIs
=========

Image
-----

APIs with the effect to one single image.

GET
^^^

*Not available.*

PUT
^^^

Used for upload new image.

Example in *CURL*:

.. code-block:: bash

    curl -X PUT \
        http://image.local-domain:5000/api/v0/image \
        -H 'content-type: multipart/form-data' \
        -F 'file=@/path/to/your/image.png;type=image/png' \
        -F username=1a339c02-404a-4b66-9fbb-cb30fb417c14 \
        -F 'password=knwAAOfLBcnkWzGxo0G/ZUzq9ukLb+gf5H/1nmPr7BE+im03qZarW4TvwVepYmi/cg9dEw+N4HDfLqQRfXBSdNawy7YkOQgwOYiRRq3t2PSjYd+Pme4SrMWUE1BYW5rt' \
        -F 'description=Image #1'

Parameters:

- **username**: This is required.
- **password**: This is required.
- **description**: image's description in string. This is optional.
- **file**: Image type file. This is required.

The above command would get result from server similar to this:

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

New created image can be viewed at
*http://image.local-domain:5000/serve/image/1/ca4ffe9f192f4f358e4981ceaafd8068.jpg*.

POST
^^^^

Used to update an image's description.

Example in *CURL*:

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

Parameters:

- **username**: This is required.
- **password**: This is required.
- **filename**: Image file's name. This is required.
- **description**: Image's description in string.
  This is optional. (If there is no description available
  then the file's description will be delete.)

Result:

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

DELETE
^^^^^^

Used to delete an image.

Example in *CURL*:

.. code-block:: bash

    curl -X DELETE \
          http://image.local-domain:5000/api/v0/image \
          -H 'content-type: application/json' \
          -d '{
            "username": "1a339c02-404a-4b66-9fbb-cb30fb417c14",
            "password": "knwAAOfLBcnkWzGxo0G/ZUzq9ukLb+gf5H/1nmPr7BE+im03qZarW4TvwVepYmi/cg9dEw+N4HDfLqQRfXBSdNawy7YkOQgwOYiRRq3t2PSjYd+Pme4SrMWUE1BYW5rt",
            "filename": "ca4ffe9f192f4f358e4981ceaafd8068.jpg",
          }'

Parameters:

- **username**: This is required.
- **password**: This is required.
- **filename**: Image file's name. This is required.

Images
------

APIs that can interact with multiple images.

GET
^^^

*Not available.*

PUT
^^^

*Not available.*

POST
^^^^

Fetch an list of images uploaded by requesting user. Each page will return
items limited by *IMAGEBUTLER_API_IMAGES_LIMIT* configuration.

Example in *CURL*:

.. code-block:: bash

    curl -X POST \
        http://image.local-domain:5000/api/v0/images \
        -H 'content-type: application/json' \
        -d {
            "username": "1a339c02-404a-4b66-9fbb-cb30fb417c14",
            "password": "knwAAOfLBcnkWzGxo0G/ZUzq9ukLb+gf5H/1nmPr7BE+im03qZarW4TvwVepYmi/cg9dEw+N4HDfLqQRfXBSdNawy7YkOQgwOYiRRq3t2PSjYd+Pme4SrMWUE1BYW5rt",
            "page": 0
        }

Parameter:

- **username**: This is required.
- **password**: This is required.
- **page**: page number of the return list. This is optional (0).
- **locale**: this will decide the format of some return attribute.
  For example: created_date. This is optional (en).
- **search**: keyword which will be used to look for in the description.

DELETE
^^^^^^

*Not available.*
