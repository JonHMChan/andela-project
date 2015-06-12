from flask import Flask
app = Flask(__name__)

# Home Page
@app.route('/')
def hello_world():
    return 'Hello Andela!'

# An individual link
@app.route('/comment')
def comment():
  return 'Comments'

# Posting a link
@app.route('/posts')
def post():
  return 'Post things here'

# Commenting on a link
@app.route('/comment/<int:comment_id>')
def comment_link(comment_id):
  return 'Comments on a link'+ str(comment_id)

if __name__ == '__main__':
    app.run(debug = True)