from flask import Blueprint, request
from tables import *
from db import DbContainer

frauds_bp = Blueprint("frauds", __name__, url_prefix="/application/frauds")


@frauds_bp.route("/", methods=("POST", "GET"))
def report_fraud():
    if request.method == "POST":
        db = DbContainer.get_db()
        response = None
        try:
            json_request = request.get_json()
            wniosek = db.session.query(Wnioski).filter(Wnioski.numer_wniosku == json_request["applicationId"])

            if wniosek is not None:
                if wniosek.pracownik_id is None:
                    raise Exception(f"The porpopsal with id [{wniosek.numerWniosku}] has no staff memmber assigned.")
                fraud_report = Zgloszenia(powod=json_request["reason"], organScigania=json_request["authority"])
                db.session.add(fraud_report)
                db.session.flush()

                wniosek.zgloszenie = fraud_report.id
                wniosek.decyzja = 'ZGLOSZONY'
                db.session.commit()
                response = {"success": 1}, 200
            else:
                raise Exception(f"No proposal found for given id - {json_request['applicationId']}.")

        except Exception as e:
            response = {"error": f"Invalid request: {str(e)}"}, 400
            print("An error occurred. Performing rollback...")
            db.session.rollback()
            db.session.close()
    else:
        response = {"error": f"Unsupported mehtod: \"{request.method}\"."}, 405

    return response
