"""Defining types which will be used to store serving objects."""

from flask import make_response


class ImageServingObject(object):

    def __init__(self, mime, content, thumbnail):
        self.mime = mime
        self.content = content
        self.thumbnail = thumbnail

    def make_response(self, is_thumbnail=False):
        response = make_response(
            self.content if not is_thumbnail else self.thumbnail)
        response.headers['Content-Type'] = self.mime
        return response
