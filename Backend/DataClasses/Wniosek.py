class Wniosek:
    numerWniosku = None
    decyzja = None
    klient = None
    wskPrzeterminowania = None
    wsparcieInnejKomorki = None
    kwota = None
    rodzajWeryfikacji = None
    zgloszenie = None

    def __init__(self, numerWniosku, decyzja, klient, wskPrzeterminowania, wsparcieInnejKomorki, kwota,
                 rodzajWeryfikacji, zgloszenie):
        self.numerWniosku = numerWniosku
        self.decyzja = decyzja
        self.wskPrzeterminowania = wskPrzeterminowania
        self.wsparcieInnejKomorki = wsparcieInnejKomorki
        self.kwota = kwota
        self.rodzajWeryfikacji = rodzajWeryfikacji
        self.zgloszenie = zgloszenie
        self.klient = klient



