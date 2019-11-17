from flask import Flask, g
import psycopg2
from flask_sqlalchemy import SQLAlchemy
import config


def get_db():
    if "db" not in g:
        app = get_app()
        db = SQLAlchemy(app)
        db.init_app(app)

        g.db = db

    return g.db


def get_app():
    if "app" not in g:
        app = Flask("__main__")
        app.config['SECRET_KEY'] = 'ken sent  me'
        app.config['DEBUG'] = True
        # app.config.from_object(os.environ['APP_SETTINGS'])
        app.config['SQLALCHEMY_DATABASE_URI'] = config.DB_URL
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        g.app = app

    return g.app


def close_db(e=None):
    db = g.pop("db", None)

    if db is not None:
        db.Close()
