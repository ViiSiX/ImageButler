"""Docstring for image_butler.views module."""

from flask import jsonify, make_response
from .imagebutler import app
from .models import ImageModel


@app.route('/')
@app.route('/serve')
@app.route('/serve/image')
def index_view():
    """Return a JSON that specific what will this application do."""
    
    return jsonify({
        'application': 'ImageButler',
        'description': 'This application allow user to upload images using REST API'
                       ' and serving those images to the Internet users.',
        'versions': {
            'api': '0'
        }
    })


@app.route('/serve/image/<int:user_id>/<string:file_name>')
def image_view(user_id, file_name):
    im = ImageModel.query.\
        filter_by(user_id=user_id, file_name=file_name).first()
    if im is not None:
        response = make_response(im.file_content)
        response.headers['Content-Type'] = im.file_mime
        return response
    else:
        return jsonify({'error': 'Not a single image found!'})
