from Backend.DataClasses.Uzytkownik import Uzytkownik
from Backend.DataClasses.IKlient import IKlient


class KlientFirmowy(Uzytkownik, IKlient):
    nazwa = None
    nip = None
    klientFirmowy_id = None

    def __init__(self, uzytkownik, nazwa, nip, klientFirmowy_id):
        Uzytkownik.Uzytkownik.__init__(self, uzytkownik)
        self.nazwa = nazwa
        self.nip = nip
        self.klientFirmowy_id = klientFirmowy_id

    def GetId(self):
        return self.klientFirmowy_id
