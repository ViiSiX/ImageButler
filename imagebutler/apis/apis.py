"""Import libraries and some predefined variables."""

from flask import Blueprint
from flask_restful import Api
from ..imagebutler import config


API_BP = Blueprint('api_v0',
                   __name__,
                   url_prefix='/api/v{0}'.
                   format(config['IMAGEBUTLER_API_VERSION']))
api = Api(API_BP)  # pylint: disable=invalid-name
