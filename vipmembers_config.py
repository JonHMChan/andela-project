from flask import request, render_template, abort, jsonify
from flask.ext.login import current_user
from setup import app
from models import *
PAGINATION_VIEWS_PER_PAGE = 12



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
        return abort(404);


@app.route('/vipmembers')
@app.route('/vipmembers/<int:page>')
def vipMembers(page=1):
    link = User.query.paginate(page, PAGINATION_VIEWS_PER_PAGE, False)
    return render_template('vip/index.html', link=link)