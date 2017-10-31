from flask import Flask, Blueprint
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)

# The configuration must be loaded before other modules.
app.config.from_object('imagebutler.settings.BaseConfig')
app.config.from_envvar('IMAGEBUTLER_CONFIGS', silent=True)

# Initial others app level extension instances
config = app.config
api_bp = Blueprint('api_v0',
                   __name__,
                   url_prefix='/api/{0}'.
                   format(config['IMAGEBUTLER_API_VERSION']))
api = Api(api_bp)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
