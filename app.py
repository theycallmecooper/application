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

@app.route('/signup')
def signup():
    return render_template('signup.html')



if __name__ == '__main__':
    app.run(debug=True)
    @app.route('/signup', methods=['GET', 'POST'])
    def signup():
        if request.method == "POST":
            #retrieve the form data
            username = request.form.get('username')
            password = request.form.get('password')

            #check if the username already exists
            existing_user = db_session.query(User).filter_by(username=username).first()
            if existing_user:
                flash("Username already taken. Please choose a different one.")
                return redirect(url_for('signup'))

            #create a new user and add to the database
            new_user = User(username=username)
            new_user.set_password(password)  # assuming User model has set_password method
            db_session.add(new_user)
            db_session.commit()

            flash("User registered successfully. Please log in.", "info")
            return redirect(url_for('login'))
        
        return render_template('signup.html')