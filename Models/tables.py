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
