"""APIs used for more than one image at the same time."""

from babel.dates import format_datetime
from flask_restful import Resource, reqparse
from .apis import config
from ..models import ImageModel, UserModel
from ..utils import user_identity_check


class Images(Resource):
    """Images REST API. POST for getting a list of images."""

    parsers = {
        'POST': reqparse.RequestParser()
    }
    parsers['POST'].add_argument('username', required=True, type=str)
    parsers['POST'].add_argument('password', required=True, type=str)
    parsers['POST'].\
        add_argument('page', required=False, type=int, default=0)
    parsers['POST'].\
        add_argument('locale', required=False, type=str, default='en')
    parsers['POST'].\
        add_argument('search', required=False, type=str, default='')

    def post(self):
        """POST: Getting a list of owning images"""
        args = self.parsers['POST'].parse_args()
        user = UserModel.query.filter_by(user_name=args.username).first()

        uic = user_identity_check(user, args.password)
        if not uic[0]:
            return uic[1]

        return_object = {}

        images_query = ImageModel.query.filter_by(user_id=user.user_id)
        if args.search:
            images_query = images_query.filter(
                ImageModel.file_description.like("%" + args.search + "%")
            )
        images = images_query.order_by('id').\
            limit(config['IMAGEBUTLER_API_IMAGES_LIMIT']).\
            offset(args.page*config['IMAGEBUTLER_API_IMAGES_LIMIT']).all()
        for image in images:
            return_object[image.image_id] = {
                'filename': image.file_name,
                'description': image.file_description,
                'mime_type': image.file_mime,
                'created_date': format_datetime(
                    image.created_on,
                    locale=args.locale
                )
            }
        return {'return': {'success': return_object}}
