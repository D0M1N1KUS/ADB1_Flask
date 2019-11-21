import functools, json, datetime
from db import DbContainer
from tables import Uzytkownicy, Adresy, Wnioski, Pracownicy
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

        q = db.session.query(Wnioski.numer_wniosku, Uzytkownicy.imie, Uzytkownicy.nazwisko, Wnioski.data,
                             Wnioski.typ_kredytu, Wnioski.kwota)\
            .filter(Wnioski.uzytkownik_id == Uzytkownicy.id)

        ret_json = []
        for row in q:
            wniosek_json = {
                "id": 0,
                "applicationId": row[0],
                "client": {
                  "firstName": row[1],
                  "lastName": row[2]
                },
                "data": row[3].strftime("%Y-%m-%d %H:%M:%S"),
                "type": row[4],
                "amount": row[5]
            }
            ret_json.append(wniosek_json)

        return json.dumps(ret_json)
    else:
        return {"error": "Unsupported method"}


@proposals_bp.route("/add", methods=("PUT", "POST", "GET"))
def add_proposal():
    if request.method == "POST" or request.method == "PUT":
        response = None
        db = DbContainer.get_db()
        try:
            json_request = request.get_json()
            parse_result = AddProposalParser.parse(json_request)
            if parse_result is not None:
                raise Exception(parse_result)

            user = db.session.query(Uzytkownicy.id)\
                .filter(Uzytkownicy.imie == json_request["firstName"])\
                .filter(Uzytkownicy.nazwisko == json_request["lastName"])\
                .first()

            home_address = db.session.query(Adresy)\
                .filter(Adresy.miasto == json_request["homeStreet"])\
                .filter(Adresy.ulica == json_request["homeCity"])\
                .filter(Adresy.kod_pocztowy == json_request["homePostalCode"]).first()

            mailing_address = db.session.query(Adresy)\
                .filter(Adresy.miasto == json_request["mailingStreet"])\
                .filter(Adresy.ulica == json_request["mailingCity"])\
                .filter(Adresy.kod_pocztowy == json_request["mailingPostalCode"]).first()

            if user is None:
                new_home_address = Adresy(ulica=json_request["homeStreet"], miasto=json_request["homeCity"],
                                          kodPocztowy=json_request["homePostalCode"])

                if home_address is None or not home_address == new_home_address:
                    home_address = new_home_address
                    db.session.add(home_address)

                new_mailing_address = Adresy(ulica=json_request["mailingStreet"], miasto=json_request["mailingCity"],
                                            kodPocztowy=json_request["mailingPostalCode"])

                if (mailing_address is None or not mailing_address == new_mailing_address and
                        not new_mailing_address == new_home_address):
                    mailing_address = new_mailing_address
                    db.session.add(mailing_address)
                else:
                    mailing_address = home_address

                db.session.flush()

                user = Uzytkownicy(imie=json_request["firstName"], nazwisko=json_request["lastName"],
                                         pesel=json_request["pesel"], adresZamieszkania=home_address.id,
                                         adresZameldowania=mailing_address.id, pracownik=None, login=None,
                                         haslo=None)
                db.session.add(user)
                db.session.flush()

            date_to_insert = datetime.datetime.utcnow()
            if "applicationId" in json_request:
                application_id = json_request["applicationId"]
            else:
                application_id = None

            new_proposal = Wnioski(numerWniosku=application_id, decyzja='ZGLOSZONY',
                                   typ_kredytu=json_request["loanType"], uzytkownik_id=user.id, zgloszeniaId=None,
                                   data=date_to_insert, kwota=json_request["amount"], pracownik_id=None)

            db.session.add(new_proposal)
            db.session.commit()
            response = {"success": 1}, 200
        except Exception as e:
            response = {"error": f"Invalid request: {str(e)}"}, 400
            print("An error occurred. Performing rollback...")
            db.session.rollback()
            db.session.close()

        return response


    else:
        return {"error": f"Unsupported method{request.method}"}, 400
