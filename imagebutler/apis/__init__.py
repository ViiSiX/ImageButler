from .apis import api
from .ping import Ping
from .image import Image


api.add_resource(Ping, '/ping')
api.add_resource(Image, '/image')
