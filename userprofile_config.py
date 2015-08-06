from flask import render_template, request, json
from flask.ext.login import login_required, current_user
from setup import app
from models import *
import cloudinary
import cloudinary.uploader
import cloudinary.api

cloudinary.config(
    cloud_name=app.config['CLOUDINARY_NAME'],
    api_key=app.config['CLOUDINARY_KEY'],
    api_secret=app.config['CLOUDINARY_SECRET']
)


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




# cloudinary file upload
@app.route('/fileUpload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['image']
        if file:
            cloudinary_res = cloudinary.uploader.upload(file, height=350, width=350, gravity='face',
                                                        allowed_formats=['jpg', 'png', 'jpeg'], crop="fill")
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
