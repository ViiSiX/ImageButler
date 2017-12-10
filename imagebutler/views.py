"""Docstring for image_butler.views module."""

from flask import jsonify
from flask_cors import cross_origin
from .imagebutler import app, rdb
from .models import ImageModel
from .job_workers import worker_do_cache_redis


@app.route('/')
@app.route('/serve')
@app.route('/serve/image')
def index_view():
    """Return a JSON that specific what will this application do."""

    return jsonify({
        'application': 'ImageButler',
        'description': 'This application allow user to upload images using '
                       'REST API and serving those images to the Internet '
                       'users.',
        'versions': {
            'api': '0'
        }
    })


@app.route('/serve/image/<int:user_id>/<string:file_name>')
@cross_origin()
def image_view(user_id, file_name):
    """Return image following requests."""

    queue = rdb.queue['serving']
    try:
        print("Serve from cache")
        print(queue.fetch_job(file_name).result)
        cached_object = queue.fetch_job(file_name).result
        return cached_object.make_response()
    except AttributeError:
        print("Serve from DB")
        im = ImageModel.query.\
            filter_by(user_id=user_id,
                      file_name=file_name,
                      is_deleted=False).first()
        if im is not None:
            if rdb.worker_process is None:
                rdb.start_worker()
            queue.enqueue(
                f=worker_do_cache_redis,
                kwargs={'caching_object': im.serving_object},
                job_id=file_name
            )
            return im.serving_object.make_response()
        else:
            return jsonify({'error': 'Not a single image found!'})


@app.route('/serve/thumbnail/<int:user_id>/<string:file_name>')
@cross_origin()
def thumbnail_view(user_id, file_name):
    """Return thumbnail of a image following requests."""

    queue = rdb.queue['serving']
    try:
        cached_object = queue.fetch_job(file_name).result
        return cached_object.make_response(is_thumbnail=True)
    except AttributeError:
        im = ImageModel.query. \
            filter_by(user_id=user_id,
                      file_name=file_name,
                      is_deleted=False).first()
        if im is not None:
            if rdb.worker_process is None:
                rdb.start_worker()
            queue.enqueue(
                f=worker_do_cache_redis,
                kwargs={'caching_object': im.serving_object},
                job_id=file_name
            )
            return im.serving_object.make_response(is_thumbnail=True)
        else:
            return jsonify({'error': 'Not a single image found!'})
