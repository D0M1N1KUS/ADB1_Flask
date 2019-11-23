from db import DbContainer
from sqlalchemy import UniqueConstraint

t_db = DbContainer.get_db()


class Zgloszenia(t_db.Model):
    __tablename__ = 'zgloszenia'

    id = t_db.Column(t_db.Integer, primary_key=True, autoincrement=True)
    powod = t_db.Column(t_db.VARCHAR)
    organ_scigania = t_db.Column(t_db.VARCHAR)

    wnioski_rel = t_db.relationship("Wnioski", backref="zgloszenia", uselist=False)

    def __init__(self, powod, organScigania):
        self.powod = powod
        self.organ_scigania = organScigania

    def __repr__(self):
        return '<id {}'.format(self.id)


class Czynnosci(t_db.Model):
    __tablename__ = 'czynnosci'

    nazwa = t_db.Column(t_db.VARCHAR, primary_key=True)
    punktacja = t_db.Column(t_db.Integer)

    aktywnosci_rel = t_db.relationship("Aktywnosci", backref="czynnosci", uselist=False)

    UniqueConstraint('nazwa', name='uix_1')

    def __init__(self, nazwa, punktacja):
        self.nazwa = nazwa
        self.punktacja = punktacja

    def __repr__(self):
        return '<id {}'.format(self.id)


class Aktywnosci(t_db.Model):
    __tablename__ = 'aktywnosci'

    id = t_db.Column(t_db.Integer, primary_key=True, autoincrement=True)
    data_aktywnosci = t_db.Column(t_db.DateTime)
    id_pracownika = t_db.Column(t_db.Integer, t_db.ForeignKey('pracownicy.id'))
    nazwa_czynnosci = t_db.Column(t_db.VARCHAR, t_db.ForeignKey('czynnosci.nazwa'))

    czynnosci_rel = t_db.relationship("Czynnosci", backref="aktywnosci", uselist=False)

    def __init__(self, dataAktywnosci, idPracownika, nazwaCzynnosci):
        self.dataAktywnosci = dataAktywnosci
        self.idPracownika = idPracownika
        self.nazwa_czynnosci = nazwaCzynnosci

    def __repr__(self):
        return '<id {}'.format(self.id)


class Pracownicy(t_db.Model):
    __tablename__ = 'pracownicy'

    id = t_db.Column(t_db.Integer, primary_key=True, autoincrement=True)
    stanowisko = t_db.Column(t_db.VARCHAR)

    uzytkownicy_rel = t_db.relationship("Uzytkownicy", backref="pracownicy", uselist=False)
    aktywnosci_rel = t_db.relationship("Aktywnosci", backref="pracownicy")
    wnioski_rel = t_db.relationship("Wnioski", backref="pracownicy")

    def __init__(self, stanowisko):
        self.stanowisko = stanowisko

    def __repr__(self):
        return '<id {}'.format(self.id)


class Adresy(t_db.Model):
    __tablename__ = 'adresy'

    id = t_db.Column(t_db.Integer, primary_key=True, autoincrement=True)
    ulica = t_db.Column(t_db.VARCHAR)
    miasto = t_db.Column(t_db.VARCHAR)
    kod_pocztowy = t_db.Column(t_db.VARCHAR)

    def __init__(self, ulica, miasto, kodPocztowy):
        self.ulica = ulica
        self.miasto = miasto
        self.kod_pocztowy = kodPocztowy

    def __repr__(self):
        return '<id {}'.format(self.id)

    def __eq__(self, other):
        try:
            return (self.ulica == other.ulica and
                    self.miasto == other.miasto and
                    self.kod_pocztowy == other.kod_pocztowy)
        except:
            return False


class Uzytkownicy(t_db.Model):
    __tablename__ = 'uzytkownicy'

    id = t_db.Column(t_db.Integer, primary_key=True, autoincrement=True)
    imie = t_db.Column(t_db.VARCHAR)
    nazwisko = t_db.Column(t_db.VARCHAR)
    pesel = t_db.Column(t_db.VARCHAR)
    adres_zamieszkania = t_db.Column(t_db.Integer, t_db.ForeignKey('adresy.id'))
    adres_zameldowania = t_db.Column(t_db.Integer, t_db.ForeignKey('adresy.id'))
    pracownik = t_db.Column(t_db.Integer, t_db.ForeignKey('pracownicy.id'),
                            nullable=True)  # if null the user is a customer
    login = t_db.Column(t_db.VARCHAR)
    haslo = t_db.Column(t_db.VARCHAR)

    pracownicy_rel = t_db.relationship("Pracownicy", backref="uzytkownicy", uselist=False)
    wnioski_rel = t_db.relationship("Wnioski", backref="uzytkownicy")
    adres_zamieszkania_rel = t_db.relationship("Adresy", foreign_keys=[adres_zamieszkania], uselist=False)
    adres_zameldowania_rel = t_db.relationship("Adresy", foreign_keys=[adres_zameldowania], uselist=False)

    def __init__(self, imie, nazwisko, pesel, adresZamieszkania, adresZameldowania, login, haslo, pracownik):
        self.imie = imie
        self.nazwisko = nazwisko
        self.pesel = pesel
        self.adres_zamieszkania = adresZamieszkania
        self.adres_zameldowania = adresZameldowania
        self.login = login
        self.haslo = haslo
        self.pracownik = pracownik

    def __repr__(self):
        return '<id {}'.format(self.id)


class Wnioski(t_db.Model):
    __tablename__ = 'wnioski'

    numer_wniosku = t_db.Column(t_db.Integer, primary_key=True, autoincrement=True)
    decyzja = t_db.Column(t_db.VARCHAR)

    uzytkownik_id = t_db.Column(t_db.Integer, t_db.ForeignKey('uzytkownicy.id'), nullable=True)
    zgloszenie_id = t_db.Column(t_db.Integer, t_db.ForeignKey('zgloszenia.id'), nullable=True)
    pracownik_id = t_db.Column(t_db.Integer, t_db.ForeignKey('pracownicy.id'), nullable=True)

    data = t_db.Column(t_db.DateTime)
    kwota = t_db.Column(t_db.FLOAT(precision=2))
    typ_kredytu = t_db.Column(t_db.VARCHAR, nullable=True)

    uzytkownik_rel = t_db.relationship("Uzytkownicy", foreign_keys=[uzytkownik_id], backref="wnioski")
    pracownik_rel = t_db.relationship("Pracownicy", foreign_keys=[pracownik_id], backref="wnioski")
    zgloszenia_rel = t_db.relationship("Zgloszenia", backref="wnioski", uselist=False)

    def __init__(self, numerWniosku, decyzja, uzytkownik_id, pracownik_id, data, kwota, typ_kredytu, zgloszeniaId):
        self.decyzja = decyzja
        self.uzytkownik_id = uzytkownik_id
        self.pracownik_id = pracownik_id
        self.data = data
        self.kwota = kwota
        self.typ_kredytu = typ_kredytu
        self.zgloszenie_id = zgloszeniaId
        self.numer_wniosku = numerWniosku

    def __repr__(self):
        return '<id {}'.format(self.id)
