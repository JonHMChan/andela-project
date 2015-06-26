from flask import Flask

app = Flask(__name__)
app.secret_key = 'development'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://demorole1:password1@localhost/nowwehere'