import functools, json
from db import DbContainer
from tables import Uzytkownicy, Hasla, Adresy, Wnioski, Klienci, Pracownicy
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from flask import Blueprint, redirect, session, request, flash, jsonify, g
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from sqlalchemy.orm import sessionmaker, aliased
from sqlalchemy import create_engine
import config

proposals_bp = Blueprint("proposals", __name__, url_prefix="/application/proposals")


@proposals_bp.route("/", methods=("POST", "GET"))
def get_proposals():
    if request.method == "GET":
        db = DbContainer.get_db()

        u_pracownik = aliased(Uzytkownicy)
        u_klient = aliased(Uzytkownicy)
        k_klient = aliased(Klienci)
        p_pracownik = aliased(Pracownicy)

        q = db.session.query(Wnioski.numer_wniosku, Wnioski.decyzja, u_klient.imie, u_klient.nazwisko,
                             u_pracownik.imie, u_pracownik.nazwisko)\
            .outerjoin(p_pracownik, Wnioski.pracownik == p_pracownik.id)\
            .outerjoin(u_pracownik, p_pracownik.id == u_pracownik.pracownik)\
            .join(k_klient, Wnioski.klient_id == k_klient.id)\
            .join(u_klient, k_klient.id_uzytkownika == u_klient.id)

        ret_json = []
        for row in q:
            wniosek_json = {
                "user_id": 0,
                "id": row[0],
                "firstNameK": row[2],
                "lastNameK": row[3],
                "firstNameP": row[4],
                "lastNameP": row[5],
                "status": row[1]
            }
            ret_json.append(wniosek_json)

        return json.dumps(ret_json)
    else:
        return {"error": "Unsupported method"}

