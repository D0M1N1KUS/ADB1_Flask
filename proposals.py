import functools, json
from db import DbContainer
from tables import Uzytkownicy, Hasla, Adresy
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from flask import Blueprint, redirect, session, request, flash, jsonify, g
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import config

proposals_bp = Blueprint("proposals", __name__, url_prefix="application/proposals")


@proposals_bp.route("/", methods=("POST", "GET"))
def get_proposals():
    if request.method == "GET":
        db = DbContainer.get_db()

    else:
        return {"error": "Unsupported method"}

