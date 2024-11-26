from flask import Flask, render_template, request, flash, session, redirect, url_for
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from setup_db import User, Task  # Ensure User and Task models are defined in setup_db

app = Flask(__name__)
app.secret_key = '#sigmarizz23#'

# Setup the database engine and session
engine = create_engine('sqlite:///todo.db')
Session = sessionmaker(bind=engine)
db_session = Session()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        # Retrieve the form data
        username = request.form.get('username')
        password = request.form.get('password')

        # Query the database to find the user with the given username
        user = db_session.query(User).filter_by(username=username).first()

        # Check if the user exists and the password is correct
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['username'] = user.username
            flash("User logged in successfully.", "info")
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid username or password.", "error")
    
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        # Retrieve the form data
        username = request.form.get('username')
        password = request.form.get('password')

        # Check if the username already exists
        existing_user = db_session.query(User).filter_by(username=username).first()
        if existing_user:
            flash("Username already taken. Please choose a different one.", "warning")
            return redirect(url_for('signup'))

        # Create a new user and add to the database
        new_user = User(username=username)
        new_user.set_password(password)  # Assuming User model has set_password method
        db_session.add(new_user)
        db_session.commit()

        flash("User registered successfully. Please log in.", "info")
        return redirect(url_for('login'))
    
    return render_template('signup.html')

@app.route('/dashboard')
def dashboard():
    if "user_id" not in session:
        flash("Please log in to access the dashboard.", "warning")
        return redirect(url_for('login'))

    tasks = db_session.query(Task).filter_by(user_id=session['user_id']).all()
    return render_template('dashboard.html', tasks=tasks)

@app.route('/add_todo', methods=["POST"])
def add_todo(): 
    if "user_id" not in session:
        flash("Please log in to add a to-do.", "warning")
        return redirect(url_for('login'))

    task_description = request.form.get("task")
    user_id = session["user_id"]

    new_task = Task(description=task_description, user_id=user_id)
    db_session.add(new_task)
    db_session.commit()

    flash("To-Do added successfully!", "success")
    return redirect(url_for('dashboard'))

@app.route('/delete_todo/<int:todo_id>', methods=["POST"])
def delete_todo(todo_id): 
    if "user_id" not in session:
        flash("Please log in to delete a to-do.", "warning")
        return redirect(url_for('login'))
    
    task = db_session.query(Task).get(todo_id)

    if task and task.user_id == session["user_id"]:
        db_session.delete(task)
        db_session.commit()
        flash("To-Do deleted successfully!", "success")
    else:
        flash("To-Do not found or access denied.", "danger")
    return redirect(url_for('dashboard'))

# Add favicon route
@app.route('/favicon.ico')
def favicon():
    # Serve favicon directly from the static folder
    return redirect(url_for('static', filename='img/favicon.ico'))

# Ensure favicon is included in all templates
@app.context_processor
def inject_favicon():
    return dict(favicon_url=url_for('static', filename='img/favicon.ico'))

if __name__ == '__main__':
    app.run(debug=True)