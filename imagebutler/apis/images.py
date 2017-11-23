from .apis import Resource, reqparse, config
from ..models import ImageModel, UserModel
from ..utils import user_identity_check


parser = reqparse.RequestParser()
parser.add_argument('username', required=True, type=str)
parser.add_argument('password', required=True, type=str)
parser.add_argument('page', required=False, type=int, default=0)


class Images(Resource):
    """Images REST API. POST for getting a list of images."""

    def post(self):
        args = parser.parse_args()
        user = UserModel.query.filter_by(user_name=args.username).first()

        uic = user_identity_check(user, args.password)
        if not uic[0]:
            return uic[1]

        return_object = {}

        images = ImageModel.query.filter_by(user_id=user.user_id). \
            order_by('id').limit(config['IMAGEBUTLER_API_IMAGES_LIMIT']).\
            offset(args.page*config['IMAGEBUTLER_API_IMAGES_LIMIT']).all()
        for image in images:
            return_object[image.image_id] = {
                'filename': image.file_name,
                'description': image.file_description,
                'mimetype': image.file_mime
            }
        return {'return': {'success': return_object}}
