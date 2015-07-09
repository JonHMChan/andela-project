from setup import db, BaseQuery
from sqlalchemy.dialects.postgresql import JSON
from datetime import datetime
from sqlalchemy_searchable import SearchQueryMixin
from sqlalchemy_utils.types import TSVectorType
from sqlalchemy_searchable import make_searchable


make_searchable()

class UserQuery(BaseQuery, SearchQueryMixin):
    pass


class User(db.Model):
    query_class = UserQuery
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String, unique=True)
    firstname = db.Column(db.Unicode(255))
    lastname = db.Column(db.Unicode(255))
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
    search_vector = db.Column(TSVectorType('firstname', 'lastname', 'major_skill'))

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
