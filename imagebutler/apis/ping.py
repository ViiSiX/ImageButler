"""Just a prototype for REST-ful."""
from .apis import Resource


class Ping(Resource):
    """You pong when you are pinged..."""

    def get(self):
        return {'returned': 'pong'}
