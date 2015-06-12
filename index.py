from flask import Flask, render_template
app = Flask(__name__)

links = [
	{
		"title": "Google",
		"url": "http://google.com/",
		"slug": "google",
    "comments": ["This is Google", "A step further"]
	},
	{
		"title": "Facebook",
		"url": "http://facebook.com/",
		"slug": "facebook",
    "comments": ["This is facebook", "A step further on facebook"]
	},
	{
		"title": "Stack Overflow",
		"url": "http://stackoverflow.com/",
		"slug": "stack-overflow",
    "comments": ["This is stackoverflow", "A step further on stackoverflow"]
	},
	{
		"title": "Andela",
		"url": "http://andela.co/",
		"slug": "andela",
    "comments": ["This is andela", "A step further at Andela"]
	}
]

# Home Page
@app.route('/')
def home():
    return render_template('index.html', links = links)

# Show Link
@app.route('/link/<link_id>')
def link(link_id):
  for link in links:
    if link["slug"] == link_id:
      return render_template('link/index.html', link = link)
  return "No link found"

  # Commenting on a link
@app.route('/link/<link_id>/comment')
def linkComment(link_id):
  for link in links:
    if link["slug"] == link_id:
      return render_template('link/comment.html', link = link)
  return "No comments found"

# Posting a link
@app.route('/link/post')
def linkPost():
  return 'Post a new link here'

if __name__ == '__main__':
    app.run(debug = True)