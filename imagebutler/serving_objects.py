"""Defining types which will be used to store serving objects."""

from flask import make_response, jsonify


class ImageServingObject(object):
    """Class that act like a middle layer to wrap up the Image Model. Provide
    the response for Flask to return to the client. This class will be stored
    in Redis database after the first serve to improve serving performance."""

    def __init__(self, mime, content, thumbnail):
        self.mime = mime
        self.content = content
        self.thumbnail = thumbnail
        self.is_delete = False

    def make_response(self, is_thumbnail=False):
        """Make a image response. If the image is delete, return a JSON
        result."""
        if not self.is_delete:
            response = make_response(
                self.content if not is_thumbnail else self.thumbnail)
            response.headers['Content-Type'] = self.mime
            return response
        return jsonify({'error': 'Not a single image found!'})

    def delete(self):
        """Mark the object as deleted. This is complex but let's it be
        for now. We will find solution later."""
        self.is_delete = True
