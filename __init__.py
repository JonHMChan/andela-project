from flask import Flask
import os

app = Flask(__name__)
app.secret_key = 'development'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ('SQLALCHEMY_DATABASE_URI')
