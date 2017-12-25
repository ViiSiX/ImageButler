"""Just a prototype for REST-ful."""

from flask_restful import Resource


class Ping(Resource):
    """You pong when you are pinged..."""

    response = 'pong'

    def get(self):
        """GET: You pong when you are pinged..."""
        return {'returned': self.response}
