"""
Upload files using this API. For prototype the authentication way
is username and password. Later we can use something like JWT or PEM file.
"""

from .apis import Resource, reqparse
from ..models import db, ImageModel, UserModel
from ..utils import user_identity_check
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


def image_return_skeleton(image_object):
    """This function will return a dict object that will be fit into
    a success response."""
    return {'return': {'success': {
            'file_name': image_object.file_name,
            'path': '/serve/image/{0}/{1}'.format(
                image_object.user_id, image_object.file_name
            ),
            'thumbnail': '/serve/thumbnail/{0}/{1}'.format(
                image_object.user_id, image_object.file_name
            ),
            'description': image_object.file_description
        }}}


class Image(Resource):
    """Image REST API. PUT for upload a new image."""

    def put(self):
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
        args = post_parser.parse_args()
        user = UserModel.query.filter_by(user_name=args.username).first()

        uic = user_identity_check(user, args.password)
        if not uic[0]:
            return uic[1]

        im = ImageModel.query.filter_by(
            file_name=args.filename,
            user_id=user.user_id
        ).first()

        if not im:
            return {'return': {'error': 'Image not found!'}}

        im.file_description = args.description
        db.session.commit()

        return image_return_skeleton(im)
