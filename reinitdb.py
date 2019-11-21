from flask import Blueprint
from db import DbContainer
from tables import *

initdb_bp = Blueprint("reinit")
app_bp = DbContainer.get_app()


@app_bp.before_first_request
def insert_demo_data():
    db = DbContainer.get_db()
    db.drop_all(db.engine, app_bp)
    db.create_all(db.engine, app_bp)

    db.session.add(Adresy(ulica="Jedynasta", miasto="Jedynascie", kodPocztowy="11-111"))
    db.session.add(Adresy(ulica="Dwunasta", miasto="Dwanascie", kodPocztowy="12-121"))
    db.session.add(KlienciIndywidualni())
    db.session.add(KlienciIndywidualni())

    db.session.commit()

    db.session.add(Klienci())
    db.session.add(Klienci())

