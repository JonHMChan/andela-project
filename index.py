from flask import Flask, render_template
app = Flask(__name__)

links = [
	{
		"title": "Google",
		"url": "http://google.com/",
		"slug": "google"
	},
	{
		"title": "Facebook",
		"url": "http://facebook.com/",
		"slug": "facebook"
	},
	{
		"title": "Stack Overflow",
		"url": "http://stackoverflow.com/",
		"slug": "stack-overflow"
	},
	{
		"title": "Andela",
		"url": "http://andela.co/",
		"slug": "andela"
	}
]

# Home Page
@app.route('/')
def home():
    return render_template('index.html', links = links)

# An individual link
@app.route('/link/<link_id>')
def link(link_id):
	for link in links:
		if link["slug"] == link_id:
  			return render_template('link/index.html', link = link)
  	return 'No link found'

# Commenting on a link
@app.route('/link/<link_id>/comment')
def linkComment(link_id):
  return render_template('link/comment.html')

# Posting a link
@app.route('/link/post')
def linkPost():
  return 'Post a new link here'

if __name__ == '__main__':
    app.run(debug = True)