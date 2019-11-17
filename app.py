
from flask import Flask, render_template, request, url_for, redirect
# from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api
from flask_httpauth import HTTPBasicAuth
import config
import jinja2

# Remember to install the necessary stuff: pip install -r requirements.txt

# db = get_db()

# Data model

#
# class Zgloszenia(db.Model):
#     __tablename__ = 'zgloszenia'
#
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=True)
#     powod = db.Column(db.VARCHAR)
#     organScigania = db.Column(db.VARCHAR)
#
#     def __init__(self, powod, organScigania):
#         self.powod = powod
#         self.organScigania = organScigania
#
#     def __repr__(self):
#         return '<id {}'.format(self.id)
#
#
# class Czynnosci(db.Model):
#     __tablename__ = 'czynnosci'
#
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=True)
#     nazwa = db.Column(db.VARCHAR)
#     punktacja = db.Column(db.Integer)
#
#     def __init__(self, nazwa, punktacja):
#         self.nazwa = nazwa
#         self.punktacja = punktacja
#
#     def __repr__(self):
#         return '<id {}'.format(self.id)
#
#
# class Aktywnosci(db.Model):
#     __tablename__ = 'aktywnosci'
#
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=True)
#     dataAktywnosci = db.Column(db.DateTime)
#     idPracownika = db.Column(db.Integer, db.ForeignKey('pracownicy.id'))
#
#     def __init__(self, dataAktywnosci, idPracownika):
#         self.dataAktywnosci = dataAktywnosci
#         self.idPracownika = idPracownika
#
#     def __repr__(self):
#         return '<id {}'.format(self.id)
#
#
# class Pracownicy(db.Model):
#     __tablename__ = 'pracownicy'
#
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=True)
#     # aktywnosci = db.relationship('aktywnosci', backref='pracownicy', lazy=True)
#     login = db.Column(db.VARCHAR)
#     stanowisko = db.Column(db.VARCHAR)
#     uzytkownik = db.Column(db.INTEGER)
#
#     def __init__(self, stanowisko, uzytkownik):
#         self.stanowisko = stanowisko
#         self.uzytkownik = uzytkownik
#
#     def __repr__(self):
#         return '<id {}'.format(self.id)
#
#
# class Adresy(db.Model):
#     __tablename__ = 'adresy'
#
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=True)
#     ulica = db.Column(db.VARCHAR)
#     miasto = db.Column(db.VARCHAR)
#     kodPocztowy = db.Column(db.VARCHAR)
#
#     def __init__(self, ulica, miasto, kodPocztowy):
#         self.ulica = ulica
#         self.miasto = miasto
#         self.kodPocztowy = kodPocztowy
#
#     def __repr__(self):
#         return '<id {}'.format(self.id)
#
#
# class Uzytkownicy(db.Model):
#     __tablename__ = 'uzytkownicy'
#
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=True)
#     imie = db.Column(db.VARCHAR)
#     nazwisko = db.Column(db.VARCHAR)
#     pesel = db.Column(db.VARCHAR)
#     adresZamieszkania = db.Column(db.Integer, db.ForeignKey('adresy.id'), nullable=True)  # TODO: remove nullable
#     adresZameldowania = db.Column(db.Integer, db.ForeignKey('adresy.id'), nullable=True)  # TODO: remove nullable
#     login = db.Column(db.VARCHAR)
#     haslo = db.Column(db.VARCHAR)
#
#     def __init__(self, imie, nazwisko, pesel, adresZamieszkania, adresZameldowania, login, haslo):
#         self.imie = imie
#         self.nazwisko = nazwisko
#         self.pesel = pesel
#         self.adresZamieszkania = adresZamieszkania
#         self.adresZameldowania = adresZameldowania
#         self.login = login
#         self.haslo = haslo
#
#     def __repr__(self):
#         return '<id {}'.format(self.id)
#
#
# class KlienciIndywidualni(db.Model):
#     __tablename__ = 'klienciindywidualni'
#
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=True)
#     klient = db.relationship('klienci')
#
#     def __init__(self):
#         pass
#
#     def __repr__(self):
#         return '<id {}'.format(self.id)
#
#
# class Klienci(db.Model):
#     __tablename__ = 'klienci'
#
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=True)
#     idUzytkownika = db.Column(db.Integer, db.ForeignKey('uzytkownicy.id'))
#     idFirmy = db.Column(db.Integer, db.ForeignKey('firmy.id'))
#     idKlientaIndywidualnego = db.Column(db.Integer, db.ForeignKey('klienciindywidualni.id'))
#
#     def __init__(self, idUzytkownika, idFilmy, idKlientaIndywidualnego):
#         self.idUzytkownika = idUzytkownika
#         self.idFirmy = idFilmy
#         self.idKlientaIndywidualnego = idKlientaIndywidualnego
#
#     def __repr__(self):
#         return '<id {}'.format(self.id)
#
#
# class Firmy(db.Model):
#     __tablename__ = 'firmy'
#
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=True)
#     nazwa = db.Column(db.VARCHAR)
#     nip = db.Column(db.VARCHAR)
#
#     def __init__(self, nazwa, nip):
#         self.nazwa = nazwa
#         self.nip = nip
#
#     def __repr__(self):
#         return '<id {}'.format(self.id)
#
#
# class Wnioski(db.Model):
#     __tablename__ = 'wnioski'
#
#     numerWniosku = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=True)
#     decyzja = db.Column(db.VARCHAR)
#     klient = db.Column(db.Integer, db.ForeignKey('klienci.id'))
#     pracownik = db.Column(db.Integer, db.ForeignKey('pracownicy.id'), nullable=True)
#     wskPrzeterminowania = db.Column(db.DateTime)
#     kwota = db.Column(db.FLOAT(precision=2))
#     rodzajWeryfikacji = db.Column(db.VARCHAR, nullable=True)
#     zgloszenieId = db.Column(db.Integer, nullable=True)
#
#     def __init__(self, decyzja, klient, pracownik, wskPrzetwarzania, kwota, rodzajWeryfikacji, zgloszeniaId):
#         self.decyzja = decyzja
#         self.klient = klient
#         self.pracownik = pracownik
#         self.wskPrzeterminowania = wskPrzetwarzania
#         self.kwota = kwota
#         self.rodzajWeryfikacji = rodzajWeryfikacji
#         self.zgloszenieId = zgloszeniaId
#
#     def __repr__(self):
#         return '<id {}'.format(self.id)
#
#
# class Hasla(db.Model):
#     __tablename__ = 'hasla'
#
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=True)
#     haslo = db.Column(db.VARCHAR)
#     id_uzytkownika = db.Column(db.Integer, db.ForeignKey('pracownicy.id'))
#
#     def __init__(self, haslo, id_uzytkownika):
#         self.haslo = haslo
#         self.id_uzytkownika = id_uzytkownika
#
#     def __repr__(self):
#         return '<id {}'.format(self.id)
#

# @auth.verify_password
# def verify(username, password):
#     if not (username and password):
#         return
#
#
# class SomeResource(Resource):
#     @auth.login_required
#     def get(self):
#         return {"meaning_of_life": 42}


# routes
# @app.route('/')
# def index():
#     return render_template('index.html')
#
#
# @app.route('/wnioski/dodajWniosek/', methods=['POST', 'GET'])
# def wnioski():
#     if request.method == 'POST':
#
#         adresZameldowania = Adresy(
#                 ulica=request.form['az_ulica'],
#                 miasto=request.form['az_miasto'],
#                 kodPocztowy=request.form['az_kod_pocztowy']
#         )
#
#         adresKorespondencji = Adresy(
#             ulica=request.form['ak_ulica'],
#             miasto=request.form['ak_miasto'],
#             kodPocztowy=request.form['ak_kod_pocztowy']
#         )
#
#         uzytkownik = Uzytkownicy(
#             imie=request.form['imie'],
#             nazwisko=request.form['nazwisko'],
#             pesel=request.form['pesel'],
#             adresZameldowania=adresZameldowania,
#             adresZamieszkania=adresKorespondencji
#         )
#
#         exists = db.session.query(db.exists().where(Uzytkownicy.imie == uzytkownik.imieb and
#                                                     Uzytkownicy.nazwisko == uzytkownik.nazwisko and
#                                                     Uzytkownicy.pesel == uzytkownik.pesel))
#         try:
#             if not exists:
#                 db.session.add(adresZameldowania)
#                 db.session.add(adresKorespondencji)
#                 db.session.flush()
#
#                 uzytkownik.adresZameldowania = adresZameldowania.id
#                 uzytkownik.adresZamieszkania = adresKorespondencji.id
#                 db.session.add(uzytkownik)
#
#             klienci = None
#             if request.form['typ_klienta'] == 'indywidualny':
#                 klient = KlienciIndywidualni()
#                 db.session.add(klient)
#                 db.session.flush()
#
#                 klienci = Klienci(uzytkownik.id, None, klient.id)
#             else:
#                 klient = Firmy(
#                     nazwa=request.form['imie'],
#                     nip='Co to nip?'
#                 )
#                 db.session.add(klient)
#                 db.session.flush()
#
#                 klienci = Klienci(uzytkownik.id, klient.id, None)
#                 db.session.add(klienci)
#
#         except:
#             'Nieudana próba dodawania nowego uzytkownika!'
#
#         # nowyWniosek = Wnioski(
#         #     decyzja="StatusWniosku.NIEROZPATRZONY",
#         #     klient=None,
#         #     pracownik=None,
#         #     wskPrzetwarzania=datetime.utcnow(),
#         #     kwota=2.5,
#         #     rodzajWeryfikacji='brak',
#         #     zgloszeniaId=None
#         # )
#
#         try:
#             db.session.commit()
#             return redirect('/wnioski')
#         except:
#             'Niepowodzenie podczas dodawania klienta!'
#     else:
#         wnioski = db.session.query(Klienci, Uzytkownicy).innerjoin(Klienci.id == Uzytkownicy.id)
#         return render_template('wnioski.html')

app = get_app()

if __name__ == '__main__':
    # app = Flask(__name__, instance_relative_config=True)
    app.run(debug=True)


