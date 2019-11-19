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
        self.organScigania = organScigania

    def __repr__(self):
        return '<id {}'.format(self.id)


class Czynnosci(t_db.Model):
    __tablename__ = 'czynnosci'

    # id = t_db.Column(t_db.Integer, primary_key=True, autoincrement=True)
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
    login = t_db.Column(t_db.VARCHAR)
    stanowisko = t_db.Column(t_db.VARCHAR)
    uzytkownik = t_db.Column(t_db.INTEGER)

    uzytkownicy_rel = t_db.relationship("Uzytkownicy", backref="pracownicy", uselist=False)
    aktywnosci_rel = t_db.relationship("Aktywnosci", backref="pracownicy")

    def __init__(self, stanowisko, uzytkownik, login):
        self.stanowisko = stanowisko
        self.uzytkownik = uzytkownik
        self.login

    def __repr__(self):
        return '<id {}'.format(self.id)


class Adresy(t_db.Model):
    __tablename__ = 'adresy'

    id = t_db.Column(t_db.Integer, primary_key=True, autoincrement=True)
    ulica = t_db.Column(t_db.VARCHAR)
    miasto = t_db.Column(t_db.VARCHAR)
    kod_pocztowy = t_db.Column(t_db.VARCHAR)
    # uzytkownicy_rel = t_db.relationship("Uzytkownicy", foreign_keys=[adresZamieszkania], backref="adresy", uselist=False)

    def __init__(self, ulica, miasto, kodPocztowy):
        self.ulica = ulica
        self.miasto = miasto
        self.kod_pocztowy = kodPocztowy

    def __repr__(self):
        return '<id {}'.format(self.id)


class Uzytkownicy(t_db.Model):
    __tablename__ = 'uzytkownicy'

    id = t_db.Column(t_db.Integer, primary_key=True, autoincrement=True)
    imie = t_db.Column(t_db.VARCHAR)
    nazwisko = t_db.Column(t_db.VARCHAR)
    pesel = t_db.Column(t_db.VARCHAR)
    adres_zamieszkania = t_db.Column(t_db.Integer, t_db.ForeignKey('adresy.id'))
    adres_zameldowania = t_db.Column(t_db.Integer, t_db.ForeignKey('adresy.id'))
    pracownik = t_db.Column(t_db.Integer, t_db.ForeignKey('pracownicy.id'), nullable=True)
    login = t_db.Column(t_db.VARCHAR)
    haslo = t_db.Column(t_db.VARCHAR)

    pracownicy_rel = t_db.relationship("Pracownicy", backref="uzytkownicy", uselist=False)
    adres_zamieszkania_rel = t_db.relationship("Adresy", foreign_keys=[adres_zamieszkania], uselist=False)
    adres_zameldowania_rel = t_db.relationship("Adresy", foreign_keys=[adres_zameldowania], uselist=False)
    klienci_rel = t_db.relationship("Klienci", backref="uzytkownicy", uselist=False)

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


class KlienciIndywidualni(t_db.Model):
    __tablename__ = 'klienciindywidualni'

    id = t_db.Column(t_db.Integer, primary_key=True, autoincrement=True)
    klienci_rel = t_db.relationship("Klienci", backref="klienciindywidualni", uselist=False)

    def __init__(self):
        pass

    def __repr__(self):
        return '<id {}'.format(self.id)


class Klienci(t_db.Model):
    __tablename__ = 'klienci'

    id = t_db.Column(t_db.Integer, primary_key=True, autoincrement=True)
    id_uzytkownika = t_db.Column(t_db.Integer, t_db.ForeignKey('uzytkownicy.id'), nullable=True)
    id_firmy = t_db.Column(t_db.Integer, t_db.ForeignKey('firmy.id'), nullable=True)
    id_klienta_indywidualnego = t_db.Column(t_db.Integer, t_db.ForeignKey('klienciindywidualni.id'))

    uztykownicy_rel = t_db.relationship("Uzytkownicy", backref="klienci", uselist=False)
    wnioski_rel = t_db.relationship("Wnioski", backref="klienci")
    klienci_indywidualni_rel = t_db.relationship("KlienciIndywidualni", backref="klienci", uselist=False)
    firmy_rel = t_db.relationship("Firmy", backref="klienci", uselist=False)

    def __init__(self, idUzytkownika, idFilmy, idKlientaIndywidualnego):
        self.id_uzytkownika = idUzytkownika
        self.id_firmy = idFilmy
        self.id_klienta_indywidualnego = idKlientaIndywidualnego

    def __repr__(self):
        return '<id {}'.format(self.id)


class Firmy(t_db.Model):
    __tablename__ = 'firmy'

    id = t_db.Column(t_db.Integer, primary_key=True, autoincrement=True)
    nazwa = t_db.Column(t_db.VARCHAR)
    nip = t_db.Column(t_db.VARCHAR)

    klienci_rel = t_db.relationship("Klienci", backref="firmy", uselist=False)

    def __init__(self, nazwa, nip):
        self.nazwa = nazwa
        self.nip = nip

    def __repr__(self):
        return '<id {}'.format(self.id)


class Wnioski(t_db.Model):
    __tablename__ = 'wnioski'

    numer_wniosku = t_db.Column(t_db.Integer, primary_key=True, autoincrement=True)
    decyzja = t_db.Column(t_db.VARCHAR)
    klient_id = t_db.Column(t_db.Integer, t_db.ForeignKey('klienci.id'), nullable=True)
    zgloszenie_id = t_db.Column(t_db.Integer, t_db.ForeignKey('zgloszenia.id'), nullable=True)
    pracownik = t_db.Column(t_db.Integer, t_db.ForeignKey('pracownicy.id'), nullable=True)

    wsk_przeterminowania = t_db.Column(t_db.DateTime)
    kwota = t_db.Column(t_db.FLOAT(precision=2))
    rodzaj_weryfikacji = t_db.Column(t_db.VARCHAR, nullable=True)

    klient_rel = t_db.relationship("Klienci", backref="wnioski")
    zgloszenia_rel = t_db.relationship("Zgloszenia", backref="wnioski", uselist=False)

    def __init__(self, numerWniosku, decyzja, klient, pracownik, wskPrzetwarzania, kwota, rodzajWeryfikacji, zgloszeniaId):
        self.decyzja = decyzja
        self.klient_id = klient
        self.pracownik = pracownik
        self.wsk_przeterminowania = wskPrzetwarzania
        self.kwota = kwota
        self.rodzaj_weryfikacji = rodzajWeryfikacji
        self.zgloszenie_id = zgloszeniaId
        self.numer_wniosku = numerWniosku

    def __repr__(self):
        return '<id {}'.format(self.id)


class Hasla(t_db.Model):
    __tablename__ = 'hasla'

    id = t_db.Column(t_db.Integer, primary_key=True, autoincrement=True)
    haslo = t_db.Column(t_db.VARCHAR)
    id_uzytkownika = t_db.Column(t_db.Integer, t_db.ForeignKey('pracownicy.id'))

    def __init__(self, haslo, id_uzytkownika):
        self.haslo = haslo
        self.id_uzytkownika = id_uzytkownika

    def __repr__(self):
        return '<id {}'.format(self.id)

