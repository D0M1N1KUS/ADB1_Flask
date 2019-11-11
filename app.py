from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api
import config

# Remember to install the necessary stuff: pip install -r requirements.txt

app = Flask(__name__)

app.config['DEBUG'] = True
# app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_DATABASE_URI'] = config.DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
db.init_app(app)

api = Api(app)

#
# @app.route('/')
# def index():
#     return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
