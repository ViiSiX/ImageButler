"""Initial for the application."""

from .imagebutler import app, config
from .apis import API_BP, __version__ as api_version
from . import models
from . import apis, commands, views


__version__ = '0.1.0rc0'

config['VERSION'] = __version__
config['API_VERSION'] = api_version
app.register_blueprint(API_BP)
