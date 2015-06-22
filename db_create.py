from index import db
from models import UserPost

#create the database
db.create_all()

#insert data
db.session.add(UserPost("First Language", "was python, javascript"))
db.session.add(UserPost("Second Language", "was bootstrap, lua"))

#commit data
db.session.commit()