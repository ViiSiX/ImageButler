"""Initial for the application."""

from .imagebutler import app, api_bp
from . import models
from . import api, views


__version__ = '0.0.1dev'

app.register_blueprint(api_bp)
