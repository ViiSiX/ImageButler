"""Docstring for image_butler.models module."""

import datetime
from flask_login import UserMixin
from imagebutler import utils
from .imagebutler import db, config


class CustomModelMixin(object):
    """imagebutler.models.CustomModelMixin: used to created basic columns."""
    created_on = db.Column('createdOn', db.DateTime,
                           default=datetime.datetime.now)
    last_updated = db.Column('lastUpdated',
                             db.DateTime,
                             onupdate=datetime.datetime.now,
                             default=datetime.datetime.now)
    version = db.Column(db.Integer, index=False, nullable=False)
    

class User(UserMixin, CustomModelMixin, db.Model):
    """imagebutler.models.User"""
    
    # Columns definition
    user_id = db.Column('id', db.Integer,
                        primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), index=True, unique=True, nullable=False)
    user_name = db.Column('userName', db.String(255), 
                          index=True, unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    is_active = db.Column('isActive', db.Boolean,
                          nullable=False, default=False)
    last_login = db.Column('lastLogin', db.DateTime, nullable=True)

    # Relationships
    images = db.relationship('Image', backref='User', lazy='joined')
    
    def __init__(self, user_email):
        """
        Constructor for User class.
        :param user_email: User's email.
        """
        if utils.validate_email(user_email):
            self.email = user_email
        else:
            raise ValueError('Email %s is not valid!' % user_email)
        self.user_name = utils.generate_user_name()
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


class Image(CustomModelMixin, db.Model):
    """imagebutler.models.Image"""
    
    # Columns definition
    image_id = db.Column('id', db.Integer,
                         primary_key=True, autoincrement=True)
    content = db.Column('content', db.LargeBinary,
                        nullable=False)
    checksum = db.Column('contentChecksum', db.String(255),
                         nullable=False)
    user_id = db.Column('userId', db.Integer,
                        db.ForeignKey('user.id'), nullable=False)

    # Relationships

    def __init__(self, content):
        """
        Construction for Image class.

        :param content: Binary content of the Image.
        """

        self.content = content
        self.checksum = utils.get_checksum(content)
        self.version = config['IMAGEBUTLER_MODELS_VERSION']['Image']
