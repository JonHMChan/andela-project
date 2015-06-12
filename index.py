from flask import Flask
app = Flask(__name__)

# Home Page
@app.route('/')
def hello_world():
    return 'Hello Andela!'

# An individual link

# Posting a link

# Commenting on a link

if __name__ == '__main__':
    app.run(debug = True)