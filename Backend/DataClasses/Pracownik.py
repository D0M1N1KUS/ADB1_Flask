from Backend.DataClasses import Uzytkownik


class Pracownik(Uzytkownik):
    idPracownika = None
    login = None
    stanowisko = None
    rozpatrzoneWnioski = None

    def __init__(self, uzytkownik, idPracownika, login, stanowisko, rozpatrzoneWnioski):
        Uzytkownik.Uzytkownik.__inti__(self, uzytkownik)
        self.idPracownika = idPracownika
        self.login = login
        self.stanowisko = stanowisko
        self.rozpatrzoneWnioski = rozpatrzoneWnioski
