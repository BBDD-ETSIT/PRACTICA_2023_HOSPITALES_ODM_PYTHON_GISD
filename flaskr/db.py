import flask
from flask_mongoengine import MongoEngine

db = MongoEngine()
app = flask.Flask(__name__)
app.config["MONGODB_SETTINGS"] = [
    {
        "db": "hospital",
        "host": "localhost",
        "port": 27017,
        "alias": "default",
    }
]
