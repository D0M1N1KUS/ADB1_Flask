import functools, json
from db import DbContainer
from tables import Uzytkownicy, Adresy
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from flask import Blueprint, redirect, session, request, flash, jsonify, g
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import config

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

# db_engine = create_engine(config.DB_URL)


# def login_required(view):
#     """View decorator that redirects anonymous users to the login page."""
#
#     @functools.wraps(view)
#     def wrapped_view(**kwargs):
#         if g.user is None:
#             return redirect("index")
#
#         return view(**kwargs)
#
#     return wrapped_view


# @auth_bp.before_app_request
# def load_logged_in_user():
#     """If a user id is stored in the session, load the user object from
#     the database into ``g.user``."""
#     user_id = session.get("user_id")
#
#     if user_id is None:
#         g.user = None
#     else:
#         g.user = (
#             DbContainer.get_db().execute("SELECT * FROM uzytkownicy WHERE id = ?", (user_id,)).fetchone()
#         )


@auth_bp.route("/register", methods=("GET", "POST"))
def register():
    """Register a new user.

    Validates that the username is not already taken. Hashes the
    password for security.
    """
    error = None

    if request.method == "POST":
        print(request.is_json)
        json_request = request.get_json()
        username = json_request["username"]
        password = json_request["password"]
        db = DbContainer.get_db()

        if not username:
            error = "Username is required."
        elif not password:
            error = "Password is required."
        else:
            found_user = db.session.query(Uzytkownicy.login).filter(Uzytkownicy.login == username)

            if found_user is not None:
                error = "User {0} is already registered.".format(username)

        if error is None:
            # the name is available, store it in the database and go to
            # the login page
            try:
                new_address = Adresy(ulica="Jedynasta", miasto="Jedynascie", kodPocztowy="11-111")
                db.session.add(new_address)
                db.session.flush()

                address = db.session.query(Adresy).filter(
                    Adresy.ulica == "Jedynasta" and Adresy.miasto == "Jedynascie" and
                    Adresy.kod_pocztowy == "11-111").one()

                new_user = Uzytkownicy(imie="Jan", nazwisko="Kowaslki", pesel="01234567890",
                                       adresZamieszkania=address.id,
                                       adresZameldowania=address.id, login=username, haslo=password)
                db.session.add(new_user)
                db.session.commit()
                return {"registered": "true"}  # redirect("auth.login")
            except:
                print('Something went wrong')

        flash(error)
    else:
        error = "Unsupported method"

    return {"error": error}  # render_template("auth/register.html")


@auth_bp.route("/login", methods=("GET", "POST"))
def login():
    """Log in a registered user by adding the user id to the session."""
    if request.method == "POST":
        json_request = None
        # username = None
        # password = None

        try:
            json_request = request.get_json()
            username = json_request["username"]
            password = json_request["password"]
        except:
            return {"error": "Invalid request."}, 400

        db = DbContainer.get_db()
        error = None
        user = None
        try:
            user = db.session.query(Uzytkownicy).filter(Uzytkownicy.login == username).one()
        except MultipleResultsFound as e:
            print(f"Inconsistency detected: There are multiple users with the username \"{username}\"")
            print(e)
        except NoResultFound as e:
            print(e)

        if user is None:
            error = "Incorrect username."
        elif not password == user.haslo:
            error = "Incorrect password."

        if error is None:
            # store the user id in a new session and return to the index

            session.clear()
            session[user.id] = user.id
            return {"user_id": user.id}  # redirect("index")

        flash(error)

    return {"error": error}  # render_template("auth/login.html")


@auth_bp.route("/logout", methods=("POST", "GET"))
def logout():
    """Clear the current session, including the stored user id."""
    if request.method == "POST":
        json_request = None
        user_id = None
        try:
            json_request = request.get_json()
            user_id = json_request["user_id"]
        except:
            return {"error": "Invalid request data."}, 400
        db = DbContainer.get_db()
        db.session.query(Uzytkownicy, Adresy).filter(
            Uzytkownicy.adres_zamieszkania == Adresy.id
        )

        if user_id not in session:
            return {"error": "Already logged out."}, 200

        session.pop(user_id, None)

    session.clear()
    return {"user_id": user_id}  # redirect("index")

# class Authentication:
#     db = None
#     app = None
#
#     passwordHash = None
#     userName = None
#
#     def __init__(self, db, app):
#         self.db = db
#
#     @staticmethod
#     def verifyAuthToken(app, token):
#         s = Serializer(app.config['SECRET_KEY'])
#         try:
#             data = s.loads(token)
#         except SignatureExpired:
#             return None
#         except BadSignature:
#             return None
#         user = Uzytkownicy.query.get(data['id']) # hmmm, dunno if id will work here
#         return user
#
#     def generateAuthenticationToken(self, expiration=600):
#         s = Serializer(self.app.config['SECRET_KEY'], expires_in=expiration)
#         return s.dumps({'id'})
