
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI']
app.config['DEBUG'] = os.environ['DEBUG']
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
app.config['CONSUMER_KEY'] = os.environ['CONSUMER_KEY']



#------------------------DB CONFIG ---------------------#
db = SQLAlchemy(app)
db.create_all()
db.session.commit()
#-------------------------------END -----------------------#

