from flask import Flask, jsonify
from flask_cors import CORS

from .chat import bp as chat
from .training import bp as training


def create_app(config_file="config.py"):
    app = Flask(__name__)
    app.config.from_pyfile(config_file)
    CORS(app)

    @app.route("/")
    def index():
        return jsonify({
            "status": 200,
            "message": "Welcome to Chatbot"
        })

    app.register_blueprint(chat)
    app.register_blueprint(training)

    return app
