from db import DbContainer
from flask import Blueprint
from Backend.auth import auth_bp
from Backend.proposals import proposals_bp
from reinitdb import initdb_bp


app = DbContainer.get_app()
app.register_blueprint(auth_bp)
app.register_blueprint(proposals_bp)
app.register_blueprint(initdb_bp)


if __name__ == '__main__':
    app.run(debug=True)


