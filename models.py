from setup import db
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
    photo = db.Column(db.String)

    def __init__(self, uid, firstname, lastname, email, profile):
        self.uid = uid
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.profile = profile
        self.registeredOn = datetime.utcnow()

    def is_authenticated(self):
        return self.email

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<{uid}{firstname}{lastname}{email}{profile}{registeredOn}{photo}>'.format(uid=self.uid,
                                                                                          firstname=self.firstname,
                                                                                          lastname=self.lastname,
                                                                                          email=self.email,
                                                                                          profile=self.profile,
                                                                                          registeredOn=self.registeredOn,
                                                                                          photo=self.photo)

