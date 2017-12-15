"""Import libraries and some predefined variables."""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_redislite import FlaskRedis


app = Flask(__name__)  # pylint: disable=invalid-name

# The configuration must be loaded before other modules.
app.config.from_object('imagebutler.settings.BaseConfig')
app.config.from_envvar('IMAGEBUTLER_CONFIGS', silent=True)

# Initial others app level extension instances
config = app.config  # pylint: disable=invalid-name
db = SQLAlchemy(app)
migrate = Migrate(app, db)
rdb = FlaskRedis(app,
                 rq=True, rq_queues=['serving'])
