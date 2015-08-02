from flask import render_template, request, json, url_for, redirect, session, g, jsonify, abort
from flask.ext.login import login_required, login_user, LoginManager, logout_user, current_user
import os, requests, base64
from flask_oauthlib.client import OAuth
from setup import app
from models import *
import cloudinary
import cloudinary.uploader
import cloudinary.api
from flask.ext.mandrill import Mandrill

oauth = OAuth(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login_auth'
PAGINATION_VIEWS_PER_PAGE = 6

mandrill = Mandrill(app)

cloudinary.config(
    cloud_name=app.config['CLOUDINARY_NAME'],
    api_key=app.config['CLOUDINARY_KEY'],
    api_secret=app.config['CLOUDINARY_SECRET']
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


@app.before_request
def before_request():
    g.links = User.query.all()
    g.user = current_user


# --------------------------HOMEPAGE ROUTE
@app.route('/')
def home():
    return render_template('index.html', links=g.links)


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


# -----------------GITHUB CONFIG-------------------#

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
    return linkedin.authorize(callback=url_for('linkedinauthorized', _external=True))


@app.route('/linkedin/login/authorized')
def linkedinauthorized():
    resp = linkedin.authorized_response()
    if resp is None:
        return page_not_found(request.args['error_reason'])

    session['linkedin_token'] = (resp['access_token'], '')
    user = linkedin.get('people/~')
    emailaddress = linkedin.get('people/~/email-address')
    current_user_info = User.query.filter_by(email=emailaddress.data).first()
    if current_user_info is None:
        reg = User(user.data['id'], user.data['firstName'], user.data['lastName'], emailaddress.data)
        db.session.add(reg)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            raise
    else:
        login_user(current_user_info)
    return linkedin_get_redirect_email(user.data['siteStandardProfileRequest']['url'], emailaddress.data)


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
    return google.authorize(callback=url_for('googleauthorized', _external=True))


@app.route('/google/login/authorized')
def googleauthorized():
    resp = google.authorized_response()
    if resp is None:
        return page_not_found(request.args['error_reason'])
    session['google_token'] = (resp['access_token'], '')
    person = google.get('userinfo')
    current_user_info = User.query.filter_by(email=person.data['email']).first()
    if current_user_info is None:
        reg = User(person.data['id'], person.data['given_name'], person.data['family_name'], person.data['email'])
        db.session.add(reg)
        db.session.commit()
    else:
        login_user(current_user_info)
    return get_redirect_email(person.data['email'])


@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')


# ---------------------END GOOGLE CONFIG ---------------------------------#


# ---------------------TWITTER CONFIG------------------------------#


@twitter.tokengetter
def get_twitter_token():
    resp = session['twitter_oauth']
    return resp['oauth_token'], resp['oauth_token_secret']


@app.route('/twitconnect')
def login():
    callback_url = url_for('twitteroauthorized', next=request.args.get('next'))
    return twitter.authorize(callback=callback_url or request.referrer or None)


@app.route('/twitter/oauthorized')
def twitteroauthorized():
    resp = twitter.authorized_response()
    if resp is None:
        return get_redirect_email(current_user.email)
    else:
        session['twitter_oauth'] = resp
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
    return json.dumps({'status': 'Ok', 'details': [twitterlink]}) \
 \
 \
# ---------------------------END TWITTER CONFIG--------------------------#


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
    return render_template('login.html'), 404


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
        recommended_reads = request.form['recommended_reads']
        advice = request.form['advice']

        current_user_info = User.query.filter_by(email=current_user.email).first()
        current_user_info.job = job
        current_user_info.major_skill = major_skill
        current_user_info.other_skills = other_skills
        current_user_info.about = about
        current_user_info.had_known = had_known
        current_user_info.recommended_reads = recommended_reads
        current_user_info.advice = advice
        db.session.commit()
    return json.dumps({'status': 'Ok', 'details': [job, about, major_skill,
                                                   had_known]})


@app.route('/profileWeblink', methods=['POST'])
def websiteLink():
    if request.method == 'POST':
        websitelink = request.form['ajaxDataJsObj']

        current_user_info = User.query.filter_by(email=current_user.email).first()
        current_user_info.social_website = websitelink
        db.session.commit()
    return json.dumps({'status': 'Ok', 'details': [websitelink]})

    # ----------------------END USER PROFILE ROUTE CONFIG --------------------#


# -------------------------------------SEARCH QUERY CONFIG --------------------------#
@app.route('/search')
def searchQuery(page=1):
    if 'search' in request.args:
        query = request.args.get('search')
        result = MongoIndex.objects.search_text(query).paginate(page=page, per_page=PAGINATION_VIEWS_PER_PAGE)
        return render_template('search/index.html', result=result, link=g.links)
    else:
        return render_template('search/index.html')


# /search/language route
@app.route('/search/<query>')
@app.route('/search/<query>/<int:page>')
def programLangCategory(page=1, query=''):
    if len(query) > 0:
        result = MongoIndex.objects.search_text(query).paginate(page=page, per_page=PAGINATION_VIEWS_PER_PAGE)
        return render_template('search/index.html', result=result, link=g.links, query=query)
    else:
        return ''


# create route to show result on keypress
@app.route('/queryroute/<query>')
def logQuery(query=''):
    if len(query) > 0:
        result = MongoIndex.objects.search_text(query)[:5]
        return json.dumps(result)
    else:
        return ''


def MongoData():
    checkMongoIndex = MongoIndex.objects
    count = 0
    for data in checkMongoIndex:
        count += count
        return data


@app.route('/mgSync')
def elasticSync():
    getData = User.query.all()
    result = []
    fetchMongoData = MongoData()
    for data in getData:
        result.append(str(data.id))
        mIndex = MongoIndex(firstname=data.firstname, skill=data.major_skill, photo=data.photo, email=data.email)
        mIndex.save()
        if (fetchMongoData is not None):
            mIndex.delete()
            mIndex.save()
    return 'Success: ' + ",".join(result)


# ------------------------------------------END SEARCH QUERY CONFIG ----------------------------#

@app.route('/getVipCode', methods=['POST'])
def vipConfig():
    if request.method == 'POST':
        codes = ['codility', 'sugarpop', 'regex']
        coupon_form = request.form['input-code']
        current_user_info = User.query.filter_by(email=current_user.email).first()
        for code in codes:
            if code == coupon_form:
                current_user_info.vip = True
                db.session.commit()
                return jsonify({'res': code})
        return jsonify({'error': 'Code invalid'})


@app.route('/vipmembers')
@app.route('/vipmembers/<int:page>')
def vipMembers(page=1):
    link = User.query.paginate(page, PAGINATION_VIEWS_PER_PAGE, False)
    return render_template('vip/index.html', link=link)


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
