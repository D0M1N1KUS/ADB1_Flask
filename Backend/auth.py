import functools
from db import get_db
from app import Uzytkownicy, Hasla, Adresy
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from flask import Blueprint, redirect, session, request, flash, g
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


bp = Blueprint("auth", __name__, url_prefix="/auth")


def login_required(view):
    """View decorator that redirects anonymous users to the login page."""

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect("index")

        return view(**kwargs)

    return wrapped_view


@bp.before_app_request
def load_logged_in_user():
    """If a user id is stored in the session, load the user object from
    the database into ``g.user``."""
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = (
            get_db().execute("SELECT * FROM uzytkownicy WHERE id = ?", (user_id,)).fetchone()
        )


@bp.route("/register", methods=("GET", "POST"))
def register():
    """Register a new user.

    Validates that the username is not already taken. Hashes the
    password for security.
    """
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        error = None

        if not username:
            error = "Username is required."
        elif not password:
            error = "Password is required."
        elif (
            db.execute("SELECT id FROM uzytkownicy WHERE username = ?", (username,)).fetchone()
            is not None
        ):
            error = "User {0} is already registered.".format(username)

        if error is None:
            # the name is available, store it in the database and go to
            # the login page
            try:
                dbase = declarative_base()
                session_maker = sessionmaker(db)
                reg_session = session_maker()
                dbase.metadata.create_all(db)

                new_address = Adresy(ulica="Jedynasta", miasto="Jedynascie", kodPocztowy="11-111")
                reg_session.add(new_address)
                reg_session.flush()

                address = reg_session.query(Adresy).filter(Adresy.ulica == "Jedynasta" and Adresy.miasto == "Jedynascie" and
                                             Adresy.kodPocztowy == "11-111").one()

                new_user = Uzytkownicy(imie="Jan", nazwisko="Kowaslki", pesel="01234567890", adresZamieszkania=address.id,
                                       adresZameldowania=address.id, login=username, password=password)
                reg_session.add(new_user)
                reg_session.commit()
                return {"registered": "true"}  # redirect("auth.login")
            except:
                'Something went wrong'

        flash(error)

    return {"registered": "false"}  # render_template("auth/register.html")


@bp.route("/login", methods=("GET", "POST"))
def login():
    """Log in a registered user by adding the user id to the session."""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        error = None
        user = db.execute(
            "SELECT * FROM uzytkownicy WHERE login = ?", (username,)
        ).fetchone()

        if user is None:
            error = "Incorrect username."
        elif not password == user.haslo:
            error = "Incorrect password."

        if error is None:
            # store the user id in a new session and return to the index
            session.clear()
            session["user_id"] = user["id"]
            return {"login": "true"}  # redirect("index")

        flash(error)

    return {"login": "false"}  # render_template("auth/login.html")


@bp.route("/logout")
def logout():
    """Clear the current session, including the stored user id."""
    session.clear()
    return redirect("index")

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

