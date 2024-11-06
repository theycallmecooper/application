from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():

    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Homepage</title>
    </head>
    <body>
        <h1>Welcome to the home page</h1>
        <p>You can go and read about us on our <a href='./about'>about</a> page!</p>
    </body>
    </html>
    '''

    return html

@app.route('/about')
def about():

    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>About</title>
    </head>
    <body>
        <h1>About page</h1>
        <p>This is the about page. To return to the home page click <a href='.'>here</a>!</p>
    </body>
    </html>
    '''

    return html

app.run(debug=True, reloader_type='stat', port=5000)