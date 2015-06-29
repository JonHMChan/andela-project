
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object('config.BaseConfig')


#------------------------DB CONFIG ---------------------#
db = SQLAlchemy(app)
db.create_all()
db.session.commit()
#-------------------------------END -----------------------#

