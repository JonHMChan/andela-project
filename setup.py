
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)
for key in os.environ.keys():
	app.config[key] = os.environ[key]


#------------------------DB CONFIG ---------------------#
db = SQLAlchemy(app)
db.create_all()
db.session.commit()
#-------------------------------END -----------------------#

