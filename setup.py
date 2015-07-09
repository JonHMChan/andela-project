from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy, BaseQuery
from sqlalchemy.orm.mapper import configure_mappers
import os

app = Flask(__name__)
for key in os.environ.keys():
    app.config[key] = os.environ[key]


# ------------------------DB CONFIG ---------------------#
db = SQLAlchemy(app)
configure_mappers()
db.create_all()
db.session.commit()
# -------------------------------END -----------------------#
