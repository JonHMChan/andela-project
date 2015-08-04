from flask import render_template, request, json, url_for, redirect, session, g, jsonify, abort
from flask.ext.login import login_user, LoginManager, logout_user, current_user
import os, requests, base64
from setup import app
from models import *
from flask.ext.mandrill import Mandrill
from collections import deque
import __init__
from social_config import socialAuth
import search_config
import vipmembers_config
import userprofile_config


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login_auth'


mandrill = Mandrill(app)


@app.before_request
def before_request():
    g.links = User.query.all()
    g.user = current_user


# --------------------------HOMEPAGE ROUTE
def limitData():
    ls = []
    count = ''
    data = User.query.filter_by(vip=User.vip).limit(8).all()
    for link in data:
        if link.vip:
            count+=count
            ls.append(link)
    return ls


@app.route('/')
def home():
    fetchData = limitData()
    return render_template('index.html', links=fetchData)


@app.route('/about')
def about():
    return render_template('about.html')


# Home Page Contact Form
@app.route('/homeContact', methods=["POST"])
def homeContactForm():
    cptKey = app.config['GOOGLE_RECAPTCHA_SECRET']
    mailto = app.config['MANDRILL_DEFAULT_EMAIL_TO']
    mailfrom = app.config['MANDRILL_DEFAULT_EMAIL_TO']

    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        subject = request.form['subject']
        message = request.form['message']
        cptResponse = request.form['g-recaptcha-response']

        googleCaptchaRequest = requests.get(
            'https://www.google.com/recaptcha/api/siteverify?secret=' + cptKey + '&response=' + cptResponse)
        response = googleCaptchaRequest.json()

        if response['success'] == True:
            mandrill.send_email(
                from_email=mailfrom,
                subject=subject,
                to=[{'email': mailto}],
                html='<p>From: ' + email + '</p><br/>---------<p>Name: ' + name + '</p>-------<br/><p>Message: ' + message + '</p>'
            )
            return json.dumps({'status': 'Ok', 'details': [cptResponse, email, subject, message]})
        else:
            return abort(401)


# ----------------------END HOMEPAGE ROUTE---------------------#

# Show Link
@app.route('/pub/<user_id>')
def link(user_id):
    # from database, retrieve user object from database
    user = User.query.get(user_id)
    if user:
        return render_template('pub/index.html', user=user)
    return "No User found"


@login_manager.user_loader
def load_user(id):
    return User.query.get(id)


@app.route('/login_auth')
def login_auth():
    return render_template('login.html')


@app.route('/logout')
def logout():
    logout_user()
    session.pop('google_token', None)
    session.pop('linkedin_token', None)
    return redirect(url_for('home'))


def get_redirect_email(email_address):
    sort = User.query.filter_by(email=email_address).first()
    login_user(sort)
    return redirect(request.args.get('next') or url_for('profile', id=sort.id,
                                                        user_id=sort.firstname.lower()))






@app.route('/devjson')
def devJson():
    response = requests.get(
        'https://api.github.com/repos/andela-bfowotade/partial-nowwehere/contents/nowwehere-tools.json?client_id=' +
        app.config['GITHUB_CONSUMER_KEY'] + '&client_secret=' + app.config['GITHUB_CONSUMER_SECRET'])
    assert response.status_code == 200
    serializeData = response.json()
    if serializeData:
        DecodeserializeData = base64.b64decode(serializeData['content'])
        return jsonify({'data': DecodeserializeData})


@app.route('/devtools')
def devRoute():
    return render_template('tools/index.html')


@app.route('/proglang')
def progLangRoute():
    return render_template('tools/proglang.html')


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
