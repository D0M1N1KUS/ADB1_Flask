from flask import Flask
import psycopg2
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
import config



class DbContainer:

    db = None
    app = None
    engine = None

    @staticmethod
    def get_db():
        if DbContainer.db is None:
            app = DbContainer.get_app()
            db = SQLAlchemy(app)
            # db.init_app(app)
            DbContainer.db = db

        return DbContainer.db

    @staticmethod
    def get_app():
        if DbContainer.app is None:
            app = Flask(__name__)
            app.config['SECRET_KEY'] = 'ken sent  me'
            app.secret_key = 'ken sent me'
            app.config['DEBUG'] = True
            # app.config.from_object(os.environ['APP_SETTINGS'])
            app.config['SQLALCHEMY_DATABASE_URI'] = config.DB_URL
            app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

            DbContainer.app = app

        return DbContainer.app

    @staticmethod
    def close_db(e=None):
        if DbContainer.db is not None:
            DbContainer.db.Close()

    @staticmethod
    def get_engine():
        if DbContainer.engine is None:
            DbContainer.engine = create_engine(config.DB_URL)
        return DbContainer.engine

