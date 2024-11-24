from flask import Flask, render_template, request, flash, session, redirect, url_for
# from werkzeug.security import check_password_hash
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from setup_db import User, Task #import the user and task models from the models file.

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
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid username or password.", "error")
    
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/add_todo', methods=["POST"])
def add_todo(): 
    # Ensure the user is logged in
    if "user_id" not in session:         
        flash("Please log in to add a to-do.", "warning")
        return redirect(url_for('login')) 

    # Retrieve task data from the form
    task_description = request.form.get("task")
    user_id = session["user_id"]

    # Create a new Task object and save it to the database
    new_task = Task(description=task_description, user_id=user_id)
    db_session.add(new_task)
    db_session.commit()

    flash("To-Do added successfully!", "success")
    return redirect(url_for('dashboard'))

@app.route('/delete_todo/<int:todo_id>', methods=["POST"])
def delete_todo(todo_id): 
    # Ensure the user is logged in 
    if "user_id" not in session:
        flash("Please log in to delete a to-do.", "warning") 
        return redirect(url_for('login')) 
    
    # Query the database for the task     
    task = db_session.query(Task).get(todo_id) 
    
    # Ensure the task exists and belongs to the logged-in user 
    if task and task.user_id == session["user_id"]:
        db_session.delete(task)
        db_session.commit()
        flash("To-Do deleted successfully!", "success")
    else:
        flash("To-Do not found or access denied.", "danger")
    return redirect(url_for('dashboard')) 


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