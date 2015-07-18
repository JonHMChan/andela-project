from setup import db, mongodb
from sqlalchemy.dialects.postgresql import JSON
from datetime import datetime




class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String, unique=True)
    firstname = db.Column(db.String)
    lastname = db.Column(db.String)
    email = db.Column(db.String(80), unique=True)
    registeredOn = db.Column(db.DateTime)
    photo = db.Column(db.String)
    job = db.Column(db.String)
    major_skill = db.Column(db.Unicode(50))
    other_skills = db.Column(JSON)
    about = db.Column(db.String)
    had_known = db.Column(db.String)
    advice = db.Column(db.String)
    social_website = db.Column(db.String)
    social_linkedin = db.Column(db.String)
    social_twitter = db.Column(db.String)
    social_github = db.Column(db.String)

    def __init__(self, uid, firstname, lastname, email):
        self.uid = uid
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
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
        return '<{uid}{firstname}{lastname}{email}{registeredOn}{photo}{job}{major_skill}{' \
               'other_skills}{about}{had_known}{advice}{social_website}{social_linkedin}{social_twitter}{' \
               'social_github}>'.format(
            uid=self.uid,
            firstname=self.firstname,
            lastname=self.lastname,
            email=self.email,
            registeredOn=self.registeredOn,
            photo=self.photo,
            job=self.job,
            major_skill=self.major_skill,
            other_skills=self.other_skills,
            about=self.about,
            had_known=self.had_known,
            advice=self.advice,
            social_website=self.social_website,
            social_linkedin=self.social_linkedin,
            social_twitter=self.social_twitter,
            social_github=self.social_github,
        )

class MongoIndex(mongodb.Document):
    firstname = mongodb.StringField(required=True)
    skill = mongodb.StringField(required=True, max_length=100)
    photo = mongodb.StringField(required=True)

    meta = {
        'allow_inheritance': True,
        'indexes': [{'fields': ['$firstname', '$skill', 'photo'],
           'default_language': 'english'}],
        'ordering': ['-firstname']
    }