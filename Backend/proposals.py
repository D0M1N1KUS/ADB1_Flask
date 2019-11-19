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
from Backend.Parsers.AddProposalParser import AddProposalParser
import config
import sys

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
                             u_pracownik.imie, u_pracownik.nazwisko) \
            .outerjoin(p_pracownik, Wnioski.pracownik == p_pracownik.id) \
            .outerjoin(u_pracownik, p_pracownik.id == u_pracownik.pracownik) \
            .join(k_klient, Wnioski.klient_id == k_klient.id) \
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


@proposals_bp.route("/add", methods=("PUT", "POST", "GET"))
def add_proposal():
    if request.method == "POST" or request.method == "PUT":
        error = None
        try:
            json_request = request.get_json()
            parse_result = AddProposalParser.parse(json_request)
            if parse_result is not None:
                raise Exception(parse_result)

            db = DbContainer.get_db()
            klient_pesel = json_request["pesel"]
            klient_user = db.session.query(Klienci.id).join(Uzytkownicy, Klienci.id_uzytkownika == Uzytkownicy.id)\
                .filter(Uzytkownicy.pesel == json_request["pesel"]).first()

            if klient_user is None:
                return {"error": f"Given person is not a customer or does not exist: \"{json_request['name']} {json_request['surname']}\""}

            date_to_insert = None
            if "wskPrzeterminowania" not in json_request:
                date_to_insert = datetime.datetime.utcnow()
            else:
                date_to_insert = json_request["wskPrzeterminowania"]  # datetime.datetime.strptime(json_request["wskPrzeterminowania"], '%Y-%m-%d %H:%M:%S')
            # next_month = datetime.datetime.now()+datetime.timedelta(days=30)
            new_proposal = Wnioski(numerWniosku=json_request["numerWniosku"], kwota=json_request["amount"],
                                   wskPrzetwarzania=date_to_insert, decyzja='ZGLOSZONY', klient=klient_user.id, pracownik=None,
                                   rodzajWeryfikacji=None, zgloszeniaId=None)

            db.session.add(new_proposal)
            db.session.commit()
            return {"success": 1}, 200
        except Exception as e:
            return {"error": f"Invalid request: {str(e)}"}, 400
    else:
        return {"error": f"Unsupported method{request.method}"}, 400
