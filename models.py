from index import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String, unique=True)
    firstname = db.Column(db.String)
    lastname = db.Column(db.String)
    email = db.Column(db.String(80), unique=True)
    profile = db.Column(db.String)
    registeredOn = db.Column(db.DateTime)


    def __init__(self, uid, firstname, lastname, email, profile):
        self.uid = uid
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.profile = profile
        self.registeredOn = datetime.utcnow()


    def __repr__(self):
        return '<{}>'.format(self.uid)


