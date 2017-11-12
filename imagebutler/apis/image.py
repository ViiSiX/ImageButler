"""
Upload files using this API. For prototype the authentication way
is username and password. Later we can use something like JWT or PEM file.
"""

from .apis import Resource, reqparse, config
from ..models import db, ImageModel, UserModel
from werkzeug.datastructures import FileStorage


parser = reqparse.RequestParser()
parser.add_argument('username', required=True, type=str)
parser.add_argument('password', required=True, type=str)
parser.add_argument('description', required=False, type=str)
parser.add_argument('file', required=True,
                    type=FileStorage,
                    location='files')


class Image(Resource):
    """Image REST API. POST for upload an image."""

    def post(self):
        args = parser.parse_args()
        user = UserModel.query.filter_by(user_name=args.username).first()

        # For the first prototype let's just using this method.
        if user is None:
            return {'return': {'error': 'User does not existed!'}}
        if user.password != args.password:
            return {'return': {'error': 'Authentication failed!'}}

        im = ImageModel(args.file, user.user_id,
                        file_description=args.description)
        db.session.add(im)
        db.session.commit()
        return {'return': {'success': {
            'path': '/serve/image/{0}/{1}'.format(
                im.user_id, im.file_name
            )
        }}}
