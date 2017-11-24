"""
Upload files using this API. For prototype the authentication way
is username and password. Later we can use something like JWT or PEM file.
"""

from .apis import Resource, reqparse
from ..imagebutler import rdb
from ..models import db, ImageModel, UserModel
from ..utils import user_identity_check
from ..job_workers import worker_undo_cached_redis
from werkzeug.datastructures import FileStorage


put_parser = reqparse.RequestParser()
put_parser.add_argument('username', required=True, type=str)
put_parser.add_argument('password', required=True, type=str)
put_parser.add_argument('description', required=False, type=str)
put_parser.add_argument('file', required=True,
                        type=FileStorage,
                        location='files')

post_parser = reqparse.RequestParser()
post_parser.add_argument('filename', required=True, type=str)
post_parser.add_argument('username', required=True, type=str)
post_parser.add_argument('password', required=True, type=str)
post_parser.add_argument('description', required=False, type=str)

delete_parser = reqparse.RequestParser()
post_parser.add_argument('filename', required=True, type=str)
post_parser.add_argument('username', required=True, type=str)
post_parser.add_argument('password', required=True, type=str)


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

    def put(self):
        """PUT for upload a new image."""
        args = put_parser.parse_args()
        user = UserModel.query.filter_by(user_name=args.username).first()

        uic = user_identity_check(user, args.password)
        if not uic[0]:
            return uic[1]

        im = ImageModel(args.file, user.user_id,
                        file_description=args.description)
        db.session.add(im)
        db.session.commit()
        return image_return_skeleton(im)

    def post(self):
        """POST for update image's description."""
        args = post_parser.parse_args()
        user = UserModel.query.filter_by(user_name=args.username).first()

        uic = user_identity_check(user, args.password)
        if not uic[0]:
            return uic[1]

        im = ImageModel.query.filter_by(
            file_name=args.filename,
            user_id=user.user_id,
            is_deleted=False
        ).first()

        if not im:
            return {'return': {'error': 'Image not found!'}}

        im.file_description = args.description
        db.session.commit()

        return image_return_skeleton(im)

    def delete(self):
        """DELETE for mark image as deleted, clear Image's cache."""
        args = post_parser.parse_args()
        user = UserModel.query.filter_by(user_name=args.username).first()

        uic = user_identity_check(user, args.password)
        if not uic[0]:
            return uic[1]

        im = ImageModel.query.filter_by(
            file_name=args.filename,
            user_id=user.user_id,
            is_deleted=False
        ).first()

        if not im:
            return {'return': {'error': 'Image not found!'}}

        im.is_deleted = True

        # Clear the cache.
        queue = rdb.queue['serving']
        try:
            cached_object = queue.fetch_job(im.file_name).result
            if cached_object:
                print("Cleaning cache for %s" % im.file_name)
                queue.enqueue(
                    f=worker_undo_cached_redis,
                    kwargs={'caching_object': im.serving_object},
                    job_id=im.file_name,
                    result_ttl=1
                )
        except AttributeError:
            # There is no RQ cache yet.
            pass

        db.session.commit()

        return {'return': {'success': 'Image deleted!'}}
