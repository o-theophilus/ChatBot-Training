from flask import Flask
from flask_cors import CORS

from .api import bp as api
from .api.chat import bp as chat
from .api.training import bp as training


def create_app(config_file="config.py"):
    app = Flask(__name__)
    app.config.from_pyfile(config_file)
    CORS(app)

    app.register_blueprint(api)
    app.register_blueprint(chat)
    app.register_blueprint(training)

    return app
