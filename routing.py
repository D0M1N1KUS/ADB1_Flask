from flask import Flask, render_template, request, url_for, redirect
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api

from Backend.DataClasses.StatusWniosku import StatusWniosku
from app import app, db

from Models.tables import Klienci, Uzytkownicy, Adresy, KlienciIndywidualni, Firmy


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/wnioski/dodajWniosek/', methods=['POST', 'GET'])
def wnioski():
    if request.method == 'POST':

        adresZameldowania = Adresy(
                ulica=request.form['az_ulica'],
                miasto=request.form['az_miasto'],
                kodPocztowy=request.form['az_kod_pocztowy']
        )

        adresKorespondencji = Adresy(
            ulica=request.form['ak_ulica'],
            miasto=request.form['ak_miasto'],
            kodPocztowy=request.form['ak_kod_pocztowy']
        )

        uzytkownik = Uzytkownicy(
            imie=request.form['imie'],
            nazwisko=request.form['nazwisko'],
            pesel=request.form['pesel'],
            adresZameldowania=adresZameldowania,
            adresZamieszkania=adresKorespondencji
        )

        exists = db.session.query(db.exists().where(Uzytkownicy.imie == uzytkownik.imieb and
                                                    Uzytkownicy.nazwisko == uzytkownik.nazwisko and
                                                    Uzytkownicy.pesel == uzytkownik.pesel))
        try:
            if not exists:
                db.session.add(adresZameldowania)
                db.session.add(adresKorespondencji)
                db.session.flush()

                uzytkownik.adresZameldowania = adresZameldowania.id
                uzytkownik.adresZamieszkania = adresKorespondencji.id
                db.session.add(uzytkownik)

            klienci = None
            if request.form['typ_klienta'] == 'indywidualny':
                klient = KlienciIndywidualni()
                db.session.add(klient)
                db.session.flush()

                klienci = Klienci(uzytkownik.id, None, klient.id)
            else:
                klient = Firmy(
                    nazwa=request.form['imie'],
                    nip='Co to nip?'
                )
                db.session.add(klient)
                db.session.flush()

                klienci = Klienci(uzytkownik.id, klient.id, None)
                db.session.add(klienci)

        except:
            'Nieudana próba dodawania nowego uzytkownika!'

        # nowyWniosek = Wnioski(
        #     decyzja="StatusWniosku.NIEROZPATRZONY",
        #     klient=None,
        #     pracownik=None,
        #     wskPrzetwarzania=datetime.utcnow(),
        #     kwota=2.5,
        #     rodzajWeryfikacji='brak',
        #     zgloszeniaId=None
        # )

        try:
            db.session.commit()
            return redirect('/wnioski')
        except:
            'Niepowodzenie podczas dodawania klienta!'
    else:
        wnioski = db.session.query(Klienci, Uzytkownicy).innerjoin(Klienci.id == Uzytkownicy.id)
        return render_template('wnioski.html')

