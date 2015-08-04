from flask import Flask, render_template

app = Flask(__name__)
app.secret_key = 'development'



# handle error
@app.errorhandler(404)
def page_not_found(error):
    return render_template('login.html'), 404
