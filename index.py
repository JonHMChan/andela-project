from flask import Flask
app = Flask(__name__)

# Home Page
@app.route('/')
def home():
    return 'Hello Andela!'

# An individual link
@app.route('/link/<link_id>')
def link(link_id):
  return 'This is the link: ' + str(link_id)

# Commenting on a link
@app.route('/link/<link_id>/comment')
def linkComment(link_id):
  return 'Where to comment on link: '+ str(link_id)

# Posting a link
@app.route('/link/post')
def linkPost():
  return 'Post a new link here'

if __name__ == '__main__':
    app.run(debug = True)