from flask import Blueprint, request
from random import randrange
from tables import *
from Backend.Parsers.AddFraudParser import AddFraudParser
from db import DbContainer
from Backend.DataClasses.Decyzja import Decyzja
import json, time

frauds_bp = Blueprint("frauds", __name__, url_prefix="/application/frauds")


@frauds_bp.route("/", methods=("POST", "GET"))
def report_fraud():
    if request.method == "POST":
        db = DbContainer.get_db()
        engine = DbContainer.get_engine()
        connection = engine.connect()

        response = None
        try:
            json_request = request.get_json()
            parse_result = AddFraudParser.parse(json_request)

            if parse_result is not None:
                raise Exception(parse_result)

            wniosek = db.session.query(Wnioski)\
                .filter(Wnioski.numer_wniosku == json_request["applicationId"]).with_for_update().first()

            if wniosek is not None:
                #connection.execute("LOCK zgloszenia EXCLUSIVE")
                if wniosek.pracownik_id is None:
                    # raise Exception(f"The porpopsal with id [{wniosek.numerWniosku}] has no staff memmber assigned.")
                    staffmembers = db.session.query(Pracownicy.id).all()
                    random_staffmember = staffmembers[randrange(len(staffmembers))].id
                    print(f"No staffmember assigned to proposal with id [{wniosek.numer_wniosku}].\
                     Assigning random staffmember with id [{random_staffmember}].")
                    wniosek.pracownik_id = random_staffmember
                if wniosek.decyzja == Decyzja.ZGLOSZONY:
                    raise Exception(f'The proposal with id [{wniosek.numer_wniosku}] has already been reported!')
                fraud_report = Zgloszenia(powod=json_request["reason"], organScigania=json_request["authority"])
                db.session.add(fraud_report)
                db.session.flush()

                time.sleep(5)
                wniosek.zgloszenie_id = fraud_report.id
                wniosek.decyzja = Decyzja.ZGLOSZONY
                db.session.commit()
                response = {"success": 1}, 200
            else:
                raise Exception(f"No proposal found for given id [{json_request['applicationId']}].")

        except Exception as e:
            response = {"error": f"Invalid request: {str(e)}"}, 400
            print(e)
            print("An error occurred. Performing rollback...")
            db.session.rollback()
            db.session.close()
        #finally:
            #connection.execute("UNLOCK TABLES")
    elif request.method == "GET":
        db = DbContainer.get_db()
        q = db.session.query(Wnioski, Uzytkownicy.imie, Uzytkownicy.nazwisko, Zgloszenia.powod,
                             Zgloszenia.organ_scigania)\
            .join(Uzytkownicy, Wnioski.uzytkownik_id == Uzytkownicy.id)\
            .join(Zgloszenia, Wnioski.zgloszenie_id == Zgloszenia.id)

        ret_json = []
        for row in q:
            zgloszenie_json = {
                "client": {
                    "firstName": row[1],
                    "lastName": row[2]
                },
                "reason": row[3],
                "organ": row[4],
                "clientType:": "person"
            }
            ret_json.append(zgloszenie_json)

        return json.dumps(ret_json), 200
    else:
        response = {"error": f"Unsupported mehtod: \"{request.method}\"."}, 405

    return response
