class Uzytkownik:
    imie = None
    nazwisko = None
    pesel = None
    mail = None
    adresZameldowania = None
    adresZamieszkania = None

    def __init__(self, imie, nazwisko, pesel, mail, adresZamieszkania, adresZameldowania):
        self.imie = imie
        self.nazwisko = nazwisko
        self.pesel = pesel
        self.mail = mail
        self.adresZameldowania = adresZameldowania
        self.adresZamieszkania = adresZamieszkania

    def __inti__(self, uzytkownik):
        self.imie = uzytkownik.imie
        self.nazwisko = uzytkownik.nazwisko
        self.pesel = uzytkownik.pesel
        self.mail = uzytkownik.mail
        self.adresZameldowania = uzytkownik.adresZameldowania
        self.adresZamieszkania = uzytkownik.adresZamieszkania
