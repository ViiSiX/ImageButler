"""Docstring for image_butler.views module."""

from flask import jsonify
from .imagebutler import app


@app.route('/')
def index():
    """Return a JSON that specific what will this application do."""
    
    return jsonify({
        'application': 'ImageButler',
        'description': 'This application allow user to upload images using REST API'
                       ' and serving those images to the Internet users.',
        'versions': {
            'api': '0'
        }
    })
