from flask import Flask, render_template, request, request, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from setup_db import User #import the user model from the models file.

app = Flask(__name__)
app.secret_key = '#sigmarizz23#'

#setup the database engine and session
engine = create_engine('sqlite:///todo.db')
Session = sessionmaker(bind=engine)
db_session = Session()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

app.run(debug=True, reloader_type='stat', port=3000)