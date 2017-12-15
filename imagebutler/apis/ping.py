"""Just a prototype for REST-ful."""
from .apis import Resource


class Ping(Resource):
    """You pong when you are pinged..."""

    response = 'pong'

    def get(self):
        """GET: You pong when you are pinged..."""
        return {'returned': self.response}
