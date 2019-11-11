from Backend.DataClasses.Uzytkownik import Uzytkownik
from Backend.DataClasses.IKlient import IKlient


class KlientIndywidualny(Uzytkownik, IKlient):
    klientIndywidualny_id = None

    def __init__(self, uzytkownik, klientIndywidualny_id):
        Uzytkownik.Uzytkownik.__inti__(self, uzytkownik)
        self.klientIndywidualny_id = klientIndywidualny_id

    def GetId(self):
        return self.klientIndywidualny_id
