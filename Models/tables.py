from app import db
from sqlalchemy.dialects.postgresql import JSON


class Zgloszenia(db.Model):
    __tablename__ = 'zgloszenia'

    id = db.Column(db.Integer, primary_key=True)
    powod = db.Column(db.VARCHAR)
    organScigania = db.Column(db.VARCHAR)

    def __init__(self, powod, organScigania):
        self.powod = powod
        self.organScigania = organScigania

    def __repr__(self):
        return '<id {}'.format(self.id)


class Czynnosci(db.Model):
    __tablename__ = 'czynnosci'

    nazwa = db.Column(db.VARCHAR, primary_key=True)
    punktacja = db.Column(db.Integer)

    def __init__(self, nazwa, punktacja):
        self.nazwa = nazwa
        self.punktacja = punktacja

    def __repr__(self):
        return '<id {}'.format(self.id)


class Aktywnosci(db.Model):
    __tablename__ = 'aktywnosci'

    id = db.Column(db.Integer, primary_key=True)
    dataAktywnosci = db.Column(db.DateTime)
    idPracownika = db.Column(db.Integer, db.ForeignKey('pracownicy.id'))

    def __init__(self, dataAktywnosci, idPracownika):
        self.dataAktywnosci = dataAktywnosci
        self.idPracownika = idPracownika

    def __repr__(self):
        return '<id {}'.format(self.id)


class Pracownicy(db.Model):
    __tablename__ = 'pracownicy'

    id = db.Column(db.Integer, primary_key=True)
    # aktywnosci = db.relationship('aktywnosci', backref='pracownicy', lazy=True)
    login = db.Column(db.VARCHAR)
    stanowisko = db.Column(db.VARCHAR)
    uzytkownik = db.Column(db.INTEGER)

    def __init__(self, login, stanowisko, uzytkownik):
        self.login = login
        self.stanowisko = stanowisko
        self.uzytkownik = uzytkownik

    def __repr__(self):
        return '<id {}'.format(self.id)


class Adresy(db.Model):
    __tablename__ = 'adresy'

    id = db.Column(db.Integer, primary_key=True)
    ulica = db.Column(db.VARCHAR)
    miasto = db.Column(db.VARCHAR)
    kodPocztowy = db.Column(db.VARCHAR)

    def __init__(self, ulica, miasto, kodPocztowy):
        self.ulica = ulica
        self.miasto = miasto
        self.kodPocztowy = kodPocztowy

    def __repr__(self):
        return '<id {}'.format(self.id)


class Uzytkownicy(db.Model):
    __tablename__ = 'uzytkownicy'

    id = db.Column(db.Integer, primary_key=True)
    imie = db.Column(db.VARCHAR)
    nazwisko = db.Column(db.VARCHAR)
    pesel = db.Column(db.VARCHAR)
    adresZamieszkania = db.Column(db.Integer, db.ForeignKey('adresy.id'))
    adresZameldowania = db.Column(db.Integer, db.ForeignKey('adresy.id'))

    def __init__(self, imie, nazwisko, pesel, adresZamieszkania, adresZameldowania):
        self.imie = imie
        self.nazwisko = nazwisko
        self.pesel = pesel
        self.adresZamieszkania = adresZamieszkania
        self.adresZameldowania = adresZameldowania

    def __repr__(self):
        return '<id {}'.format(self.id)


class KlienciIndywidualni(db.Model):
    __tablename__ = 'klienciindywidualni'

    id = db.Column(db.Integer, primary_key=True)
    klient = db.relationship('kleinci')

    def __init__(self):
        x = 0

    def __repr__(self):
        return '<id {}'.format(self.id)


class Klienci(db.Model):
    __tablename__ = 'klienci'

    id = db.Column(db.Integer, primary_key=True)
    idUzytkownika = db.Column(db.Integer, db.ForeignKey('uzytkownicy.id'))
    idFilmy = db.Column(db.Integer, db.ForeignKey('firmy.id'))
    idKlientaIndywidualnego = db.Column(db.Integer, db.ForeignKey('klienciindywidualni.id'))

    def __init__(self, idUzytkownika, idFilmy, idKlientaIndywidualnego):
        self.idUzytkownika = idUzytkownika
        self.idFilmy = idFilmy
        self.idKlientaIndywidualnego = idKlientaIndywidualnego

    def __repr__(self):
        return '<id {}'.format(self.id)


class Firmy(db.Model):
    __tablename__ = 'firmy'

    id = db.Column(db.Integer, primary_key=True)
    nazwa = db.Column(db.VARCHAR)
    nip = db.Column(db.VARCHAR)

    def __init__(self, nazwa, nip):
        self.nazwa = nazwa
        self.nip = nip

    def __repr__(self):
        return '<id {}'.format(self.id)


class Wnioski(db.Model):
    __tablename__ = 'wnioski'

    numerWniosku = db.Column(db.Integer, primary_key=True)
    decyzja = db.Column(db.VARCHAR)
    klient = db.Column(db.Integer)
    wskPrzeterminowania = db.Column(db.DateTime)
    kwota = db.Column(db.FLOAT(precision=2))
    rodzajWeryfikacji = db.Column(db.VARCHAR)
    zgloszenieId = db.Column(db.Integer)

    def __init__(self, devyzja, klient, wskPrzetwarzania, kwota, rodzajWeryfikacji, zgloszeniaId):
        self.decyzja = devyzja
        self.klient = klient
        self.wskPrzeterminowania = wskPrzetwarzania
        self.kwota = kwota
        self.rodzajWeryfikacji = rodzajWeryfikacji
        self.zgloszenieId = zgloszeniaId

    def __repr__(self):
        return '<id {}'.format(self.id)
