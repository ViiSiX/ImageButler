"""Initial for the application."""

from .imagebutler import app, api_bp
from . import models
from . import apis, commands, views


__version__ = '0.1.0rc0'

app.register_blueprint(api_bp)
