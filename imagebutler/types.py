"""Defining types which will be used to store serving objects."""

from flask import make_response


class ImageServingObject(object):

    def __init__(self, mime, content):
        self.mime = mime
        self.content = content

    def make_response(self):
        response = make_response(self.content)
        response.headers['Content-Type'] = self.mime
        return response
