"""This module stores all the REST API of ImageButler."""

from .apis import api, API_BP
from .ping import Ping
from .image import Image
from .images import Images


api.add_resource(Ping, '/ping')
api.add_resource(Image, '/image')
api.add_resource(Images, '/images')
