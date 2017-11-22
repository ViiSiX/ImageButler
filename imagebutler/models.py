"""Docstring for image_butler.models module."""

import datetime
from flask_login import UserMixin
from imagebutler import utils
from werkzeug.datastructures import FileStorage
from PIL import Image
from sqlalchemy.dialects.mysql import LONGBLOB
from .imagebutler import db, config
from .types import ImageServingObject


class CustomModelMixin(object):
    """imagebutler.models.CustomModelMixin: used to created basic columns."""
    created_on = db.Column('createdOn', db.DateTime,
                           default=datetime.datetime.now)
    last_updated = db.Column('lastUpdated',
                             db.DateTime,
                             onupdate=datetime.datetime.now,
                             default=datetime.datetime.now)
    version = db.Column(db.Integer, index=False, nullable=False)


class UserModel(UserMixin, CustomModelMixin, db.Model):
    """imagebutler.models.UserModel"""

    # Table name
    __tablename__ = 'user'

    # Columns definition
    user_id = db.Column('id', db.Integer,
                        primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    user_name = db.Column('userName', db.String(36, convert_unicode=False),
                          index=True, unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    is_active = db.Column('isActive', db.Boolean,
                          nullable=False, default=False)
    last_login = db.Column('lastLogin', db.DateTime, nullable=True)

    # Relationships
    images = db.relationship('ImageModel', backref='UserModel', lazy='joined')

    def __init__(self, user_email):
        """
        Constructor for User class.
        :param user_email: User's email.
        """
        if utils.validate_email(user_email):
            self.email = user_email
        else:
            raise ValueError('Email %s is not valid!' % user_email)
        self.user_name = utils.generate_uuid()
        self.password = utils.generate_password()
        self.version = config['IMAGEBUTLER_MODELS_VERSION']['User']

    @property
    def is_anonymous(self):
        """Return True if user is anonymous - Flask-Login method."""
        return False

    def get_id(self):
        """Get the user id in unicode string."""
        try:
            return unicode(self.user_id)
        except NameError:
            return str(self.user_id)

    def change_password(self):
        """Set new password for this user."""
        self.password = utils.generate_password()

    def __repr__(self):
        """Print the User instance."""
        return '<User {email} - Id {id}>'.format(
            email=self.email,
            id=self.user_id
        )


class ImageModel(CustomModelMixin, db.Model):
    """imagebutler.models.ImageModel"""

    # Table name
    __tablename__ = 'image'

    # Columns definition
    image_id = db.Column('id', db.Integer,
                         primary_key=True, autoincrement=True)
    file_name = db.Column('fileName', db.String(50),
                          index=True, nullable=False)
    file_description = db.Column('fileDescription', db.UnicodeText,
                                 nullable=True)
    file_mime = db.Column('fileMIME', db.String(55),
                          nullable=False)
    file_content = db.Column('fileContent',
                             db.LargeBinary().
                             with_variant(LONGBLOB, "mysql"),
                             nullable=False)
    file_exif = db.Column('fileEXIF', db.Binary,
                          nullable=True)
    file_thumbnail = db.Column('fileThumbnail', db.Binary,
                               nullable=True)
    file_checksum = db.Column('fileChecksum', db.String(64),
                              nullable=False)
    user_id = db.Column('userId', db.Integer,
                        db.ForeignKey('user.id'), nullable=False)

    # Relationships

    def __init__(self, file, user_id, file_description=None):
        """

        :param file:
        :type file: FileStorage
        """

        utils.validate_mime(file.mimetype)
        file_ext = file.filename.split('.')[-1]
        self.file_name = '{0}.{1}'.format(
            utils.generate_uuid().replace('-', ''),
            file_ext
        )
        self.file_description = \
            file.filename if file_description is None else file_description
        self.file_mime = file.mimetype
        self.user_id = user_id
        self.version = config['IMAGEBUTLER_MODELS_VERSION']['Image']

        # Image processing
        image = Image.open(file.stream)
        image_sio = utils.BytesIO()
        image.save(image_sio, format=image.format)
        # Set image values into the model
        self.file_exif = utils.get_image_exif(image)
        self.file_content = image_sio.getvalue()
        self.file_checksum = utils.get_checksum(self.file_content)
        image_sio.close()

        # Set thumbnail into the model
        self.file_thumbnail = self.gen_thumbnail(image)

        image.close()
        image_sio.close()

    def gen_thumbnail(self, image_instance=None):
        """

        :param image_instance:
        :type image_instance: PIL.Image.Image
        :return: BytesIO object
        """

        is_close_image_instance = False
        if not image_instance:
            image_instance = Image.open(utils.BytesIO(self.file_content))
            is_close_image_instance = True

        image_sio = utils.BytesIO()
        image_instance.thumbnail(
            config['IMAGEBUTLER_MAX_THUMBNAIL'],
            Image.ANTIALIAS
        )
        image_instance.save(image_sio, format=image_instance.format)
        if is_close_image_instance:
            image_instance.close()
        return image_sio.getvalue()

    @property
    def serving_object(self):
        return ImageServingObject(self.file_mime,
                                  self.file_content,
                                  self.file_thumbnail)
