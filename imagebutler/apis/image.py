"""
Upload files using this API. For prototype the authentication way
is username and password. Later we can use something like JWT or PEM file.
"""

from werkzeug.datastructures import FileStorage
from flask_restful import Resource, reqparse
from ..imagebutler import rdb
from ..models import db, ImageModel, UserModel
from ..utils import user_identity_check
from ..job_workers import worker_undo_cached_redis


def image_return_skeleton(image_object):
    """This function will return a dict object that will be fit into
    a success response."""

    return {
        'return': {
            'success': {
                'file_name': image_object.file_name,
                'path': '/serve/image/{0}/{1}'.format(
                    image_object.user_id, image_object.file_name
                ),
                'thumbnail': '/serve/thumbnail/{0}/{1}'.format(
                    image_object.user_id, image_object.file_name
                ),
                'description': image_object.file_description
            }
        }
    }


class Image(Resource):
    """Image REST API."""

    parsers = {
        'PUT': reqparse.RequestParser(),
        'POST': reqparse.RequestParser(),
        'DELETE': reqparse.RequestParser()
    }
    parsers['PUT'].add_argument('username', required=True, type=str)
    parsers['PUT'].add_argument('password', required=True, type=str)
    parsers['PUT'].add_argument('description', required=False, type=str)
    parsers['PUT'].add_argument('file', required=True,
                                type=FileStorage,
                                location='files')
    parsers['POST'].add_argument('filename', required=True, type=str)
    parsers['POST'].add_argument('username', required=True, type=str)
    parsers['POST'].add_argument('password', required=True, type=str)
    parsers['POST'].add_argument('description', required=False, type=str)
    parsers['DELETE'].add_argument('filename', required=True, type=str)
    parsers['DELETE'].add_argument('username', required=True, type=str)
    parsers['DELETE'].add_argument('password', required=True, type=str)

    def put(self):
        """PUT: for upload a new image."""
        args = self.parsers['PUT'].parse_args()
        user = UserModel.query.filter_by(user_name=args.username).first()

        uic = user_identity_check(user, args.password)
        if not uic[0]:
            return uic[1]

        image = ImageModel(args.file, user.user_id,
                           file_description=args.description)
        db.session.add(image)
        db.session.commit()
        return image_return_skeleton(image)

    def post(self):
        """POST: for update image's description."""
        args = self.parsers['POST'].parse_args()
        user = UserModel.query.filter_by(user_name=args.username).first()

        uic = user_identity_check(user, args.password)
        if not uic[0]:
            return uic[1]

        image = ImageModel.query.filter_by(
            file_name=args.filename,
            user_id=user.user_id,
            is_deleted=False
        ).first()

        if not image:
            return {'return': {'error': 'Image not found!'}}

        image.file_description = args.description
        db.session.commit()

        return image_return_skeleton(image)

    def delete(self):
        """DELETE: for mark image as deleted, clear Image's cache."""
        args = self.parsers['DELETE'].parse_args()
        user = UserModel.query.filter_by(user_name=args.username).first()

        uic = user_identity_check(user, args.password)
        if not uic[0]:
            return uic[1]

        image = ImageModel.query.filter_by(
            file_name=args.filename,
            user_id=user.user_id,
            is_deleted=False
        ).first()

        if not image:
            return {'return': {'error': 'Image not found!'}}

        image.is_deleted = True

        # Clear the cache.
        queue = rdb.queue['serving']
        try:
            cached_object = queue.fetch_job(image.file_name).result
            if cached_object:
                print("Cleaning cache for %s" % image.file_name)
                queue.enqueue(
                    f=worker_undo_cached_redis,
                    kwargs={'caching_object': image.serving_object},
                    job_id=image.file_name,
                    result_ttl=1
                )
        except AttributeError:
            # There is no RQ cache yet.
            pass

        db.session.commit()

        return {'return': {'success': 'Image deleted!'}}
