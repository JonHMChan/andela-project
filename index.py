from flask import Flask, render_template, request, json
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///userposts.db'

db = SQLAlchemy(app)
from models import *

links = [
    {
        "title": "Google",
        "url": "http://google.com/",
        "slug": "google",
        "name": "Addy Osmani",
        "comments": ["This is Google", "A step further"],
        "image": "img/contribs/1.jpg",
        "primary_technology": ["Javascript"],
        "secondary_technology":["EmberJs", "Engine"],
        "vip": True
    },
    {
        "title": "Facebook",
        "url": "http://facebook.com/",
        "slug": "facebook",
        "name": "Mark Zuckerberg",
        "comments": ["This is facebook", "A step further on facebook"],
        "image": "img/contribs/2.jpg",
        "primary_technology": ["PHP"],
        "secondary_technology":["C#", "jQuery"],
        "vip": True
    },
    {
        "title": "Stack Overflow",
        "url": "http://stackoverflow.com/",
        "slug": "stack-overflow",
        "name": "Jon Chan",
        "comments": ["This is stackoverflow", "A step further on stackoverflow"],
        "image": "img/contribs/johnchan.jpeg",
        "primary_technology": ["Python"],
        "secondary_technology":["C#", "AngularJs"],
        "vip": True
    },
    {
        "title": "Andela",
        "url": "http://andela.co/",
        "slug": "andela",
        "name": "Babajide Fowotade",
        "comments": ["This is andela", "A step further at Andela"],
        "image": "img/contribs/babajide.jpg",
        "primary_technology": ["Javascript"],
        "secondary_technology":["Firebase", "AngularJs", "NodeJs", "ExpressJs"],
        "vip": False
    },
    {
        "title": "CTO Andela",
        "url": "http://andela.co/",
        "slug": "dueprops",
        "name": "Obie Fernandez",
        "comments": ["This is obie", "A step further at obies"],
        "image": "img/contribs/obie.jpg",
        "primary_technology": ["Ruby on Rails"],
        "secondary_technology":["Firebase", "AngularJs", "NodeJs", "ExpressJs"],
        "vip": True
    }
]

# Home Page
@app.route('/')
def home():
    return render_template('index.html', links=links)

#Home Page Contact Form

@app.route('/homeContact', methods=["POST"])
def homeContactForm():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        subject = request.form['subject']
        message = request.form['message']
        return json.dumps({'status': 'Ok', 'details': [name, email, subject, message] })

# Show Link
@app.route('/link/<link_id>')
def link(link_id):
    posts = db.session.query(UserPost).all()
    for link in links:
        if link["slug"] == link_id:
            return render_template('link/index.html', link=link, post=posts)
    return "No link found"

#comments on a link
@app.route('/link/<link_id>/comment')
def linkComment(link_id):
    for link in links:
        if link["slug"] == link_id:
            return render_template('link/comment.html', link=link)
    return "No comments found"


# Logged in homepage
@app.route('/users/<user_id>')
def users():
    return 'Post a new link here'


@app.route('/submitComment', methods=["POST"])
def submitComment():
    if request.method == "POST":
        comment = request.form['comment']
        return json.dumps({'status': 'OK', 'comment': comment})


if __name__ == '__main__':
    app.run(debug=True)
