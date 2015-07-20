from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.mongoengine import MongoEngine
from mongoengine import connect
import os

app = Flask(__name__)
for key in os.environ.keys():
    app.config[key] = os.environ[key]

# ------------------------DB CONFIG ---------------------#
db = SQLAlchemy(app)
db.create_all()
db.session.commit()

db_user = app.config['MONGOLAB_USER']
db_password = app.config['MONGOLAB_PASSWORD']
connect(host='mongodb://'+db_user+':'+db_password+'@ds047602.mongolab.com:47602/nowdb')
mongodb = MongoEngine(app)
# -------------------------------END -----------------------#
