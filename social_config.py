from flask import request, json, url_for, redirect, session, render_template,g
from flask.ext.login import login_user, current_user
from setup import app
from models import *
from flask_oauthlib.client import OAuth
oauth = OAuth(app)


@app.before_request
def before_request():
    g.links = User.query.all()
    g.user = current_user

class socialAuth():
    github = oauth.remote_app(
        'github',
        consumer_key=app.config['GITHUB_CONSUMER_KEY'],
        consumer_secret=app.config['GITHUB_CONSUMER_SECRET'],
        request_token_params={'scope': 'user:email'},
        base_url='https://api.github.com/',
        request_token_url=None,
        access_token_method='POST',
        access_token_url='https://github.com/login/oauth/access_token',
        authorize_url='https://github.com/login/oauth/authorize'
    )

    google = oauth.remote_app(
        'google',
        consumer_key=app.config['GOOGLE_CONSUMER_KEY'],
        consumer_secret=app.config['GOOGLE_CONSUMER_SECRET'],
        request_token_params={
            'scope': 'https://www.googleapis.com/auth/userinfo.email'
        },
        base_url='https://www.googleapis.com/oauth2/v1/',
        request_token_url=None,
        access_token_method='POST',
        access_token_url='https://accounts.google.com/o/oauth2/token',
        authorize_url='https://accounts.google.com/o/oauth2/auth',
    )

    twitter = oauth.remote_app(
        'twitter',
        consumer_key=app.config['TWITTER_CONSUMER_KEY'],
        consumer_secret=app.config['TWITTER_CONSUMER_SECRET'],
        base_url='https://api.twitter.com/1.1/',
        request_token_url='https://api.twitter.com/oauth/request_token',
        access_token_url='https://api.twitter.com/oauth/access_token',
        authorize_url='https://api.twitter.com/oauth/authenticate',
    )

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


def get_redirect_email(email_address):
    sort = User.query.filter_by(email=email_address).first()
    login_user(sort)
    return redirect(request.args.get('next') or url_for('profile', id=sort.id,
                                                        user_id=sort.firstname.lower()))


# -----------------GITHUB CONFIG-------------------#

@app.route('/gitconnect')
def gitconnect():
    return socialAuth.github.authorize(callback=url_for('gitauthorized', _external=True))


@app.route('/github/login/authorized')
def gitauthorized():
    resp = socialAuth.github.authorized_response()
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error'],
            request.args['error_description']
        )
    session['github_token'] = (resp['access_token'], '')
    github_data = socialAuth.github.get('user')
    current_user_info = User.query.filter_by(email=current_user.email).first()
    current_user_info.social_github = github_data.data['html_url']
    db.session.commit()
    return get_redirect_email(current_user.email)


@socialAuth.github.tokengetter
def get_github_oauth_token():
    return session.get('github_token')


@app.route('/profileGitlink', methods=['POST'])
def githubLink():
    if request.method == 'POST':
        githublink = request.form['ajaxDataJsObj']
        current_user_info = User.query.filter_by(email=current_user.email).first()
        current_user_info.social_github = githublink
        db.session.commit()
    return json.dumps({'status': 'Ok', 'details': [githublink]})


# ------------------------END GITHUB CONFIG ----------------------#



# -------------------LINKED IN CONFIG -----------------------#

def linkedin_get_redirect_email(linkedin_info, email_address):
    sort = User.query.filter_by(email=email_address).first()
    login_user(sort)
    if sort.social_linkedin is None:
        sort.social_linkedin = linkedin_info
        db.session.commit()
    return redirect(request.args.get('next') or url_for('profile', id=sort.id,
                                                        user_id=sort.firstname.lower()))


@app.route('/linkedin/login')
def linkedinlogin():
    return socialAuth.linkedin.authorize(callback=url_for('linkedinauthorized', _external=True))


@app.route('/linkedin/login/authorized')
def linkedinauthorized():
    default_image = 'https://lh3.googleusercontent.com/0LLwXvYMpMQRF-ntK8Wx3zl1F569WxLeLeAD43Ct9g=s300-no'
    resp = socialAuth.linkedin.authorized_response()
    if resp is None:
        return page_not_found(request.args['error_reason'])

    session['linkedin_token'] = (resp['access_token'], '')
    user = socialAuth.linkedin.get('people/~')
    photo = socialAuth.linkedin.get('people/~:(picture-urls::(original))?format=json')
    emailaddress = socialAuth.linkedin.get('people/~/email-address')
    current_user_info = User.query.filter_by(email=emailaddress.data).first()
    if current_user_info is None:
        if 'values' in photo.data['pictureUrls']:
            reg = User(user.data['id'], user.data['firstName'], user.data['lastName'], emailaddress.data, photo.data['pictureUrls']['values'][0])
            db.session.add(reg)
        else:
            reg = User(user.data['id'], user.data['firstName'], user.data['lastName'], emailaddress.data, default_image)
            db.session.add(reg)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            raise
    else:
        login_user(current_user_info)
    return linkedin_get_redirect_email(user.data['siteStandardProfileRequest']['url'], emailaddress.data)


@socialAuth.linkedin.tokengetter
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


socialAuth.linkedin.pre_request = change_linkedin_query


@app.route('/profileLinkedIn', methods=['POST'])
def linkedInProfileConfig():
    if request.method == 'POST':
        linkedinProfile = request.form['ajaxDataJsObj']
        current_user_info = User.query.filter_by(email=current_user.email).first()
        current_user_info.social_linkedin = linkedinProfile
        db.session.commit()
    return json.dumps({'status': 'Ok', 'details': [linkedinProfile]})


# -----------------END LINKEDIN CONFIG --------------------------------#




# -------------------GOOGLE LOGIN CONFIG -----------------------------#

@app.route('/google/login')
def googlelogin():
    return socialAuth.google.authorize(callback=url_for('googleauthorized', _external=True))


@app.route('/google/login/authorized')
def googleauthorized():
    resp = socialAuth.google.authorized_response()
    if resp is None:
        return page_not_found(request.args['error_reason'])
    session['google_token'] = (resp['access_token'], '')
    person = socialAuth.google.get('userinfo')
    current_user_info = User.query.filter_by(email=person.data['email']).first()
    if current_user_info is None:
        reg = User(person.data['id'], person.data['given_name'], person.data['family_name'], person.data['email'],
                   person.data['picture'])
        db.session.add(reg)
        db.session.commit()
    else:
        login_user(current_user_info)
    return get_redirect_email(person.data['email'])


@socialAuth.google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')


# ---------------------END GOOGLE CONFIG ---------------------------------#


# ---------------------TWITTER CONFIG------------------------------#


@socialAuth.twitter.tokengetter
def get_twitter_token():
    resp = session['twitter_oauth']
    return resp['oauth_token'], resp['oauth_token_secret']


@app.route('/twitconnect')
def login():
    callback_url = url_for('twitteroauthorized', next=request.args.get('next'))
    return socialAuth.twitter.authorize(callback=callback_url or request.referrer or None)


@app.route('/twitter/oauthorized')
def twitteroauthorized():
    resp = socialAuth.twitter.authorized_response()
    if resp is None:
        return get_redirect_email(current_user.email)
    else:
        session['twitter_oauth'] = resp
        print resp
        current_user_info = User.query.filter_by(email=current_user.email).first()
        current_user_info.social_twitter = resp['screen_name']
        db.session.commit()
    return get_redirect_email(current_user.email)


@app.route('/profileTweetLink', methods=['POST'])
def twitterLink():
    if request.method == 'POST':
        twitterlink = request.form['ajaxDataJsObj']
        current_user_info = User.query.filter_by(email=current_user.email).first()
        current_user_info.social_twitter = twitterlink
        db.session.commit()
    return json.dumps({'status': 'Ok', 'details': [twitterlink]})
        # ---------------------------END TWITTER CONFIG--------------------------#


# handle error
@app.errorhandler(404)
def page_not_found(error):
    return render_template('login.html'), 404