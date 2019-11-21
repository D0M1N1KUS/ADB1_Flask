from flask import Blueprint, request
from tables import *
from db import DbContainer
import datetime

initdb_bp = Blueprint("reinitdb", __name__, url_prefix="/reinitdb")


@initdb_bp.route("/", methods=("POST", "GET"))
def insert_demo_data():
    if request.method == "POST" or request.method == "GET":
        print("Recreating db")

    db = DbContainer.get_db()

    try:
        db.session.query(Wnioski).delete()
        db.session.query(Uzytkownicy).delete()
        db.session.query(Zgloszenia).delete()
        db.session.query(Pracownicy).delete()
        db.session.query(Aktywnosci).delete()
        db.session.query(Czynnosci).delete()
        db.session.query(Adresy).delete()

        adres1 = Adresy(ulica="Jedynasta", miasto="Jedynascie", kodPocztowy="11-111")
        adres2 = Adresy(ulica="Dwunasta", miasto="Dwanascie", kodPocztowy="12-121")
        adres3 = Adresy(ulica="Szczesliwa", miasto="Szczesliwe", kodPocztowy="13-131")
        db.session.add(adres1)
        db.session.add(adres2)
        db.session.add(adres3)
        db.session.flush()

        uzytkownik1 = Uzytkownicy(imie="Jan", nazwisko="Kowalski", pesel="12345678901", adresZameldowania=adres1.id,
                                  adresZamieszkania=adres1.id, pracownik=None, login="janko", haslo="qaz123")
        uzytkownik2 = Uzytkownicy(imie="Czesiek", nazwisko="Szpadel", pesel="23456789012",
                                  adresZameldowania=adres2.id, adresZamieszkania=adres2.id, pracownik=None,
                                  login="czesz", haslo="123456")

        pracownik1 = Pracownicy(stanowisko="Obsluga klienta")
        pracownik2 = Pracownicy(stanowisko="Szef")

        db.session.add(uzytkownik1)
        db.session.add(uzytkownik2)
        db.session.add(pracownik1)
        db.session.add(pracownik2)
        db.session.flush()

        uzytkownik3 = Uzytkownicy(imie="Darek", nazwisko="Brzoza", pesel="34567890123",
                                  adresZameldowania=adres2.id, adresZamieszkania=adres2.id, pracownik=pracownik1.id,
                                  login="czesz", haslo="123456")
        uzytkownik4 = Uzytkownicy(imie="Jas", nazwisko="Fasola", pesel="45678901234",
                                  adresZameldowania=adres3.id, adresZamieszkania=adres3.id, pracownik=pracownik2.id,
                                  login="jasfa", haslo="flask_kiedy_spadnie_robi_trzask")

        db.session.add(uzytkownik3)
        db.session.add(uzytkownik4)
        db.session.flush()

        wniosek1 = Wnioski(numerWniosku=None, decyzja='NIEROZPATRZONY', uzytkownik_id=uzytkownik1.id,
                           pracownik_id=pracownik1.id, data=datetime.datetime.utcnow(), kwota=10000.0,
                           typ_kredytu='hipotetyczny', zgloszeniaId=None)
        wniosek2 = Wnioski(numerWniosku=None, decyzja='NEGATYWNY', uzytkownik_id=uzytkownik1.id,
                           pracownik_id=pracownik1.id, data=datetime.datetime.utcnow(), kwota=20000.0,
                           typ_kredytu='hipotetyczny', zgloszeniaId=None)
        wniosek3 = Wnioski(numerWniosku=None, decyzja='POZYTYWNY', uzytkownik_id=uzytkownik2.id,
                           pracownik_id=pracownik2.id, data=datetime.datetime.utcnow(), kwota=5000.0,
                           typ_kredytu='hipotetyczny', zgloszeniaId=None)
        wniosek4 = Wnioski(numerWniosku=None, decyzja='NIEROZPATRZONY', uzytkownik_id=uzytkownik2.id,
                           pracownik_id=pracownik2.id, data=datetime.datetime.utcnow(), kwota=100000.0,
                           typ_kredytu='hipotetyczny', zgloszeniaId=None)

        zgloszenie = Zgloszenia(powod="Za maly dochod", organScigania="policja")

        db.session.add(wniosek1)
        db.session.add(wniosek2)
        db.session.add(wniosek3)
        db.session.add(wniosek4)
        db.session.add(zgloszenie)
        db.session.flush()

        wniosek4.decyzja = "ZGLOSZONY"
        wniosek4.zgloszenie_id = zgloszenie.id

        db.session.commit()

        return {"success": 1}, 200
    except Exception as e:
        print(e)
        return {"error": str(e)}, 400
        db.session.rollback()
