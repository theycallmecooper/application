from flask import Flask, render_template, request, flash, session, redirect, url_for
# from werkzeug.security import check_password_hash
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

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        #retrieve the form data
        username = request.form.get('username')
        password = request.form.get('password')

        #query the database to find the user with given username
        user = db_session.query(User).filter_by(username=username).first()

        #check if the user exists and the password is correct
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['username'] = user.username
            flash("User logged in successfully.", "info")
            return redirect(url_for('index'))
        else:
            flash("Invalid username or password.")
    
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)