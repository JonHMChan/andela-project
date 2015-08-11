from flask import request, render_template, json, g
from setup import app
from models import *
PAGINATION_VIEWS_PER_PAGE = 14


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
        if data.major_skill != "Nothing":
            mIndex = MongoIndex(firstname=data.firstname, skill=data.major_skill, photo=data.photo, email=data.email)
            mIndex.save()
        if (fetchMongoData != None):
            mIndex.delete()
            mIndex.save()
    return 'Success: ' + ",".join(result)


# ------------------------------------------END SEARCH QUERY CONFIG ----------------------------#