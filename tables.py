from db import DbContainer

t_db = DbContainer.get_db()


class Zgloszenia(t_db.Model):
    __tablename__ = 'zgloszenia'

    id = t_db.Column(t_db.Integer, primary_key=True, autoincrement=True, nullable=True)
    powod = t_db.Column(t_db.VARCHAR)
    organScigania = t_db.Column(t_db.VARCHAR)

    def __init__(self, powod, organScigania):
        self.powod = powod
        self.organScigania = organScigania

    def __repr__(self):
        return '<id {}'.format(self.id)


class Czynnosci(t_db.Model):
    __tablename__ = 'czynnosci'

    id = t_db.Column(t_db.Integer, primary_key=True, autoincrement=True, nullable=True)
    nazwa = t_db.Column(t_db.VARCHAR)
    punktacja = t_db.Column(t_db.Integer)

    def __init__(self, nazwa, punktacja):
        self.nazwa = nazwa
        self.punktacja = punktacja

    def __repr__(self):
        return '<id {}'.format(self.id)


class Aktywnosci(t_db.Model):
    __tablename__ = 'aktywnosci'

    id = t_db.Column(t_db.Integer, primary_key=True, autoincrement=True, nullable=True)
    dataAktywnosci = t_db.Column(t_db.DateTime)
    idPracownika = t_db.Column(t_db.Integer, t_db.ForeignKey('pracownicy.id'))

    def __init__(self, dataAktywnosci, idPracownika):
        self.dataAktywnosci = dataAktywnosci
        self.idPracownika = idPracownika

    def __repr__(self):
        return '<id {}'.format(self.id)


class Pracownicy(t_db.Model):
    __tablename__ = 'pracownicy'

    id = t_db.Column(t_db.Integer, primary_key=True, autoincrement=True, nullable=True)
    # aktywnosci = t_db.relationship('aktywnosci', backref='pracownicy', lazy=True)
    login = t_db.Column(t_db.VARCHAR)
    stanowisko = t_db.Column(t_db.VARCHAR)
    uzytkownik = t_db.Column(t_db.INTEGER)

    def __init__(self, stanowisko, uzytkownik):
        self.stanowisko = stanowisko
        self.uzytkownik = uzytkownik

    def __repr__(self):
        return '<id {}'.format(self.id)


class Adresy(t_db.Model):
    __tablename__ = 'adresy'

    id = t_db.Column(t_db.Integer, primary_key=True, autoincrement=True, nullable=True)
    ulica = t_db.Column(t_db.VARCHAR)
    miasto = t_db.Column(t_db.VARCHAR)
    kodPocztowy = t_db.Column(t_db.VARCHAR)

    def __init__(self, ulica, miasto, kodPocztowy):
        self.ulica = ulica
        self.miasto = miasto
        self.kodPocztowy = kodPocztowy

    def __repr__(self):
        return '<id {}'.format(self.id)


class Uzytkownicy(t_db.Model):
    __tablename__ = 'uzytkownicy'

    id = t_db.Column(t_db.Integer, primary_key=True, autoincrement=True, nullable=True)
    imie = t_db.Column(t_db.VARCHAR)
    nazwisko = t_db.Column(t_db.VARCHAR)
    pesel = t_db.Column(t_db.VARCHAR)
    adresZamieszkania = t_db.Column(t_db.Integer, t_db.ForeignKey('adresy.id'))
    adresZameldowania = t_db.Column(t_db.Integer, t_db.ForeignKey('adresy.id'))
    login = t_db.Column(t_db.VARCHAR)
    haslo = t_db.Column(t_db.VARCHAR)

    def __init__(self, imie, nazwisko, pesel, adresZamieszkania, adresZameldowania, login, haslo):
        self.imie = imie
        self.nazwisko = nazwisko
        self.pesel = pesel
        self.adresZamieszkania = adresZamieszkania
        self.adresZameldowania = adresZameldowania
        self.login = login
        self.haslo = haslo

    def __repr__(self):
        return '<id {}'.format(self.id)


class KlienciIndywidualni(t_db.Model):
    __tablename__ = 'klienciindywidualni'

    id = t_db.Column(t_db.Integer, primary_key=True, autoincrement=True, nullable=True)
    klient = t_db.relationship('klienci.id')

    def __init__(self):
        pass

    def __repr__(self):
        return '<id {}'.format(self.id)


class Klienci(t_db.Model):
    __tablename__ = 'klienci'

    id = t_db.Column(t_db.Integer, primary_key=True, autoincrement=True, nullable=True)
    idUzytkownika = t_db.Column(t_db.Integer, t_db.ForeignKey('uzytkownicy.id'))
    idFirmy = t_db.Column(t_db.Integer, t_db.ForeignKey('firmy.id'))
    idKlientaIndywidualnego = t_db.Column(t_db.Integer, t_db.ForeignKey('klienciindywidualni.id'))

    def __init__(self, idUzytkownika, idFilmy, idKlientaIndywidualnego):
        self.idUzytkownika = idUzytkownika
        self.idFirmy = idFilmy
        self.idKlientaIndywidualnego = idKlientaIndywidualnego

    def __repr__(self):
        return '<id {}'.format(self.id)


class Firmy(t_db.Model):
    __tablename__ = 'firmy'

    id = t_db.Column(t_db.Integer, primary_key=True, autoincrement=True, nullable=True)
    nazwa = t_db.Column(t_db.VARCHAR)
    nip = t_db.Column(t_db.VARCHAR)

    def __init__(self, nazwa, nip):
        self.nazwa = nazwa
        self.nip = nip

    def __repr__(self):
        return '<id {}'.format(self.id)


class Wnioski(t_db.Model):
    __tablename__ = 'wnioski'

    numerWniosku = t_db.Column(t_db.Integer, primary_key=True, autoincrement=True, nullable=True)
    decyzja = t_db.Column(t_db.VARCHAR)
    klient = t_db.Column(t_db.Integer, t_db.ForeignKey('klienci.id'))
    pracownik = t_db.Column(t_db.Integer, t_db.ForeignKey('pracownicy.id'), nullable=True)
    wskPrzeterminowania = t_db.Column(t_db.DateTime)
    kwota = t_db.Column(t_db.FLOAT(precision=2))
    rodzajWeryfikacji = t_db.Column(t_db.VARCHAR, nullable=True)
    zgloszenieId = t_db.Column(t_db.Integer, nullable=True)

    def __init__(self, decyzja, klient, pracownik, wskPrzetwarzania, kwota, rodzajWeryfikacji, zgloszeniaId):
        self.decyzja = decyzja
        self.klient = klient
        self.pracownik = pracownik
        self.wskPrzeterminowania = wskPrzetwarzania
        self.kwota = kwota
        self.rodzajWeryfikacji = rodzajWeryfikacji
        self.zgloszenieId = zgloszeniaId

    def __repr__(self):
        return '<id {}'.format(self.id)


class Hasla(t_db.Model):
    __tablename__ = 'hasla'

    id = t_db.Column(t_db.Integer, primary_key=True, autoincrement=True, nullable=True)
    haslo = t_db.Column(t_db.VARCHAR)
    id_uzytkownika = t_db.Column(t_db.Integer, t_db.ForeignKey('pracownicy.id'))

    def __init__(self, haslo, id_uzytkownika):
        self.haslo = haslo
        self.id_uzytkownika = id_uzytkownika

    def __repr__(self):
        return '<id {}'.format(self.id)

