from flask import render_template, request, json, url_for, redirect, session, g, jsonify
from flask.ext.login import login_required, login_user, LoginManager, logout_user, current_user
import os
from dummyJson import sampleData
from flask_oauthlib.client import OAuth
from setup import app
from models import User, db
import cloudinary
import cloudinary.uploader
import cloudinary.api

oauth = OAuth(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login_auth'

cloudinary.config(
    cloud_name=app.config['CLOUDINARY_NAME'],
    api_key=app.config['CLOUDINARY_KEY'],
    api_secret=app.config['CLOUDINARY_SECRET']
)

demoJson = sampleData()
links = demoJson.content()

linkedin = oauth.remote_app(
    'linkedin',
    consumer_key=app.config['LINKEDIN_CONSUMER_KEY'],
    consumer_secret=app.config['LINKEDIN_CONSUMER_SECRET'],
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

github = oauth.remote_app(
    'github',
    consumer_key='2060136de8f6079f6d96',
    consumer_secret='0f39da4747fd987bc1749511ef8c826b9798a9ce',
    request_token_params={'scope': 'user:email'},
    base_url='https://api.github.com/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://github.com/login/oauth/access_token',
    authorize_url='https://github.com/login/oauth/authorize'
)


@app.before_request
def before_request():
    g.user = current_user


# --------------------------HOMEPAGE ROUTE
@app.route('/')
def home():
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


# ----------------------END HOMEPAGE ROUTE---------------------#

# Show Link
@app.route('/link/<link_id>')
def link(link_id):
    for link in links:
        if link["slug"] == link_id:
            return render_template('link/index.html', link=link)
    return "No link found"


@login_manager.user_loader
def load_user(id):
    return User.query.get(id)


@app.route('/login')
def login():
    return linkedin.authorize(callback=url_for('authorized', _external=True))


@app.route('/login_auth')
def login_auth():
    return render_template('login.html')


@app.route('/logout')
def logout():
    logout_user()
    session.pop('linkedin_token', None)
    return redirect(url_for('home'))

@app.route('/gitconnect')
def gitconnect():
    return github.authorize(callback=url_for('gitauthorized', _external=True))


@app.route('/github/login/authorized')
def gitauthorized():
    resp = github.authorized_response()
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error'],
            request.args['error_description']
        )
    session['github_token'] = (resp['access_token'], '')
    github_data = github.get('user')
    current_user_info = User.query.filter_by(email=current_user.email).first()
    current_user_info.social_github = github_data.data['html_url']
    db.session.commit()
    return get_redirect_email(current_user.email)

@github.tokengetter
def get_github_oauth_token():
    return session.get('github_token')


# -------------------LINKED IN CONFIG -----------------------#
def get_redirect_email(email_address):
    sort = User.query.filter_by(email=email_address).first()
    login_user(sort)
    return redirect(request.args.get('next') or url_for('profile', id=sort.id,
                                                        user_id=sort.firstname.lower()))


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
    current_user_info = User.query.filter_by(email=emailaddress.data).first()
    if current_user_info is None:
        reg = User(user.data['id'], user.data['firstName'], user.data['lastName'], emailaddress.data,
                   user.data['siteStandardProfileRequest']['url'])
        db.session.add(reg)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            raise
    else:
        login_user(current_user_info)
    return get_redirect_email(emailaddress.data)


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

# -----------------END LINKEDIN CONFIG --------------------------------#



# -----------------------USER PROFILE ROUTE CONFIG------------------#
@app.route('/user/<int:id>', strict_slashes=False)
@app.route('/user/<int:id>/<person>', strict_slashes=False)
@login_required
def profile(id, person=None):
    user = User.query.get_or_404(id)
    if current_user.firstname == user.firstname:
        if user.firstname != person:
            return render_template('users/index.html', id=id, person=user)
        return render_template('users/index.html', user=user)
    else:
        return 'Unauthorized Access'


# handle error
@app.errorhandler(404)
def page_not_found(error):
    return 'This page does not exist', 404


# cloudinary file upload
@app.route('/fileUpload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['image']
        if file:
            cloudinary_res = cloudinary.uploader.upload(file, width=350, height=350,
                                                        allowed_formats=['jpg', 'png', 'jpeg'],
                                                        transformation=[
                                                            {"overlay": "text:courier_80:Now%20We%20Here",
                                                             'crop': 'fill',
                                                             'color': "#EB5D1E", 'height': 30,
                                                             'gravity': "south_east", 'x': 8, 'y': 8}
                                                        ])
            current_user_info = User.query.filter_by(email=current_user.email).first()
            current_user_info.photo = cloudinary_res['secure_url']
            db.session.commit()
        return json.dumps({'status': 'Ok', 'details': cloudinary_res})


@app.route('/profileInfo', methods=["POST"])
def profileInfoForm():
    if request.method == "POST":
        job = request.form['job']
        about = request.form['about']
        major_skill = request.form['major_skill']
        other_skills = request.form['other_skills']
        had_known = request.form['had_known']
        advice = request.form['advice']

        current_user_info = User.query.filter_by(email=current_user.email).first()
        current_user_info.job = job
        current_user_info.major_skill = major_skill
        current_user_info.other_skills = other_skills
        current_user_info.about = about
        current_user_info.had_known = had_known
        current_user_info.advice = advice
        db.session.commit()
    return json.dumps({'status': 'Ok', 'details': [job, about, major_skill,
                                                   had_known]})


@app.route('/profileWeblink', methods=['POST'])
def websiteLink():
    if request.method == 'POST':
        websitelink = request.form['websitelink']

        current_user_info = User.query.filter_by(email=current_user.email).first()
        current_user_info.social_website = websitelink
        db.session.commit()
    return json.dumps({'status': 'Ok', 'details': [websitelink]})

    # ----------------------END USER PROFILE ROUTE CONFIG --------------------#


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
