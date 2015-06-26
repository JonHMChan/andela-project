from flask import Flask, render_template, request, json, url_for, redirect, session
from flask.ext.login import login_required,login_user, LoginManager
import requests, os
from dummyJson import sampleData
from flask_oauthlib.client import OAuth
from flask.ext.sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.config.from_object('config.BaseConfig')

db = SQLAlchemy(app)
#------------------------DB CONFIG ---------------------#
from models import *

db.create_all()
db.session.commit()
#-------------------------------END -----------------------#

oauth = OAuth(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

demoJson = sampleData()
links = demoJson.content()

linkedin = oauth.remote_app(
    'linkedin',
    consumer_key='77owz0iuacm1h8',
    consumer_secret='k7SKZUcbVvxqRYIq',
    request_token_params={
        'scope': ['r_basicprofile', 'r_emailaddress'],
        'state': 'RandomString',
    },
    base_url='https://api.linkedin.com/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://www.linkedin.com/uas/oauth2/accessToken',
    authorize_url='https://www.linkedin.com/uas/oauth2/authorization',
)

# Home Page
@app.route('/')
def home():
    if 'linkedin_token' in session:
        me = linkedin.get('people/~')
        emailadd = linkedin.get('people/~/email-address')

        print emailadd.data
    return render_template('index.html', links=links)


# Home Page Contact Form
@app.route('/homeContact', methods=["POST"])
def homeContactForm():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        subject = request.form['subject']
        message = request.form['message']
        return json.dumps({'status': 'Ok', 'details': [name, email, subject, message]})


# Show Link
@app.route('/link/<link_id>')
def link(link_id):
    for link in links:
        if link["slug"] == link_id:
            return render_template('link/index.html', link=link)
    return "No link found"

@login_manager.user_loader
def load_user(userid):
    return User.query.get(int(id))

@app.route('/login')
def login():
    return linkedin.authorize(callback=url_for('authorized', _external=True))


@app.route('/logout')
def logout():
    session.pop('linkedin_token', None)
    return redirect(url_for('home'))


@app.route('/login/authorized')
def authorized():
    resp = linkedin.authorized_response()
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['linkedin_token'] = (resp['access_token'], '')

    user = linkedin.get('people/~')
    emailaddress = linkedin.get('people/~/email-address')

    if User.query.filter_by(email=emailaddress.data).first() is None:
        reg = User(user.data['id'], user.data['firstName'], user.data['lastName'], emailaddress.data,
               user.data['siteStandardProfileRequest']['url'])
        db.session.add(reg)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            raise
    return redirect(url_for('home'))


@linkedin.tokengetter
def get_linkedin_oauth_token():
    return session.get('linkedin_token')


def change_linkedin_query(uri, headers, body):
    auth = headers.pop('Authorization')
    headers['x-li-format'] = 'json'
    if auth:
        auth = auth.replace('Bearer', '').strip()
        if '?' in uri:
            uri += '&oauth2_access_token=' + auth
        else:
            uri += '?oauth2_access_token=' + auth
    return uri, headers, body


linkedin.pre_request = change_linkedin_query


# comments on a link
@app.route('/link/<link_id>/comment')
def linkComment(link_id):
    for link in links:
        if link["slug"] == link_id:
            return render_template('link/comment.html', link=link)
    return "No comments found"


# Logged in homepage
@app.route('/users/<user_id>')
@login_required
def users():
    return 'Post a new link here'


@app.route('/submitComment', methods=["POST"])
def submitComment():
    if request.method == "POST":
        comment = request.form['comment']
        return json.dumps({'status': 'OK', 'comment': comment})


# Handle redirect
@app.route('/auth/linkedin/callback')
def authLinkedinCallback():
    code = request.args.get("code")
    if code:
        requests.post('https://www.linkedin.com/uas/oauth2/accessToken', data={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": "http://localhost:5000/",
            "client_id": "77owz0iuacm1h8",
            "client_secret": os.environ.get('LINKEDIN_API_SECRET', "")
        })


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
