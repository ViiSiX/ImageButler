"""Docstring for image_butler.models module."""

import datetime
from copy import deepcopy
from flask_login import UserMixin
from PIL import Image
from sqlalchemy.dialects.mysql import LONGBLOB
from . import utils
from .imagebutler import db, config
from .serving_objects import ImageServingObject


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
        """Print the UserModel instance."""
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
    file_size = db.Column('fileSize', db.Integer,
                          nullable=False,
                          default=0)
    is_deleted = db.Column('isDeleted', db.Boolean,
                           nullable=False, default=False)
    user_id = db.Column('userId', db.Integer,
                        db.ForeignKey('user.id'), nullable=False)

    # Relationships

    def __init__(self, file, user_id, file_description=None):
        """
        Constructor for ImageModel class.

        :param file: FileStorage object receive from the request.
        :type file: werkzeug.datastructures.FileStorage
        :param user_id: to which user this image belong.
        :param file_description: description of the uploaded file. The
        description should go along with other information in the request. If
        not provided file description will be original file name instead.
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
        # Set image values into the model
        image, self.file_content, self.file_checksum, \
            self.file_size, self.file_exif = \
            utils.process_uploaded_image(image,
                                         config['IMAGEBUTLER_MAX_IMAGE_SIZE'])

        # Set thumbnail into the model
        self.file_thumbnail = self.gen_thumbnail(image)
        image.close()

    def gen_thumbnail(self, image_instance=None):
        """
        Generate thumbnail of an given Image object.

        :param image_instance: Given image object that will be use to
        generate new thumbnail.
        :type image_instance: PIL.Image.Image
        :return: BytesIO object
        """

        # Image.copy() does not work since it do not copy the image format.
        temp_image = deepcopy(image_instance) if image_instance \
            else self.image

        image_sio = utils.BytesIO()
        temp_image.thumbnail(
            config['IMAGEBUTLER_MAX_THUMBNAIL'],
            Image.ANTIALIAS
        )
        temp_image.save(image_sio, format=temp_image.format)
        temp_image.close()
        return image_sio.getvalue()

    @property
    def image(self):
        """Return the image instance from the database or from argument."""

        return Image.open(utils.BytesIO(self.file_content))

    @property
    def serving_object(self):
        """The model will not direct serving data to Flask but rather a
        medium class."""

        return ImageServingObject(self.file_mime,
                                  self.file_content,
                                  self.file_thumbnail)

    def __repr__(self):
        """Print the ImageModel instance."""

        return '<Image {file_name} - User Id {user_id}>'.format(
            file_name=self.file_name,
            user_id=self.user_id
        )
