import functools, json, datetime
from db import DbContainer
from tables import Uzytkownicy, Hasla, Adresy, Wnioski, Klienci, Pracownicy
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from flask import Blueprint, redirect, session, request, flash, jsonify, g
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from sqlalchemy.orm import sessionmaker, aliased
from sqlalchemy import DateTime

staff_bp = Blueprint("staff", __name__, url_prefix="/application/staff")


@staff_bp.route("/", methods=["POST", "GET"])
def get_staff():
    if request.method == "GET":

    else:
        {"error": "Unsupported method"}
