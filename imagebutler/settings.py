"""Common settings for all environments (development|staging|production)."""


class BaseConfig:
    """
    These are some default configuration that will be loaded into any
    environment. For specific default configuration, please create other
    class.
    """

    # Application
    APP_NAME = "Image Butler"
    APP_SYSTEM_ERROR_SUBJECT_LINE = APP_NAME + " error"

    # Flask-SQLAlchemy
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///ImageButler.db' # This variable
    # will be set in config file, not here.
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Image Butler
    IMAGEBUTLER_MODELS_VERSION = {
        'User': 1,
        'Image': 1,
    }
    IMAGEBUTLER_API_VERSION = 0
