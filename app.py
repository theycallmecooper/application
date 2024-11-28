from flask import Flask, render_template, request, flash, session, redirect, url_for, jsonify
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Date
from datetime import datetime
from setup_db import User, Task, Category  # Ensure User and Task models are defined in setup_db

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
        username = request.form.get('username')
        password = request.form.get('password')

        # Query the database for the user
        user = db_session.query(User).filter_by(username=username).first()

        if user and user.check_password(password):  # Assuming `check_password` is implemented
            session['user_id'] = user.id
            session['username'] = user.username
            flash("User logged in successfully.", "info")

            # Redirect to the original URL (next) or dashboard
            next_url = request.args.get('next') or url_for('dashboard')
            return redirect(next_url)
        else:
            flash("Invalid username or password.", "error")

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')

        existing_user = db_session.query(User).filter_by(username=username).first()
        if existing_user:
            flash("Username already taken. Please choose a different one.", "warning")
            return redirect(url_for('signup'))

        new_user = User(username=username)
        new_user.set_password(password)  # Assuming `set_password` is implemented
        db_session.add(new_user)
        db_session.commit()

        flash("User registered successfully. Please log in.", "info")
        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/dashboard')
def dashboard():
    if "user_id" not in session:
        flash("Please log in to access the dashboard.", "warning")
        return redirect(url_for('login', next=request.url))  # Pass original URL in `next`

    tasks = db_session.query(Task).filter_by(user_id=session['user_id']).all()
    categories = db_session.query(Category).all()
    return render_template('dashboard.html', tasks=tasks, categories=categories)

@app.route('/add_todo', methods=["POST"])
def add_todo():
    if "user_id" not in session:
        flash("Please log in to add a to-do.", "warning")
        return redirect(url_for('login'))

    task_description = request.form.get("task")
    due_date_str = request.form.get("due_date")
    if not task_description.strip():
        flash("Task description cannot be empty.", "warning")
        return redirect(url_for('dashboard'))

    user_id = session["user_id"]
    due_date = datetime.strptime(due_date_str, '%Y-%m-%d') if due_date_str else None
    category_id = request.form.get("category")
    category = db_session.query(Category).get(category_id) if category_id else None
    new_task = Task(description=task_description.strip(), user_id=user_id, completed=False, due_date=due_date, category=category)
    db_session.add(new_task)
    db_session.commit()

    flash("To-Do added successfully!", "success")
    return redirect(url_for('dashboard'))

@app.route('/add_category', methods=["POST"])
def add_category():
    if "user_id" not in session:
        flash("Please log in to add a category.", "warning")
        return redirect(url_for('login'))
    category_name = request.form.get('category_name').strip()
    if category_name:
        existing_category = db_session.query(Category).filter_by(name=category_name).first()
        if not existing_category:
            new_category = Category(name=category_name)
            db_session.add(new_category)
            db_session.commit()
            flash("Category added successfully!", "success")
        else:
            flash("Category already exists.", "warning")
    else:
        flash("Category name cannot be empty.", "warning")
    return redirect(url_for('dashboard'))

@app.route('/delete_todo', methods=["POST"])
def delete_todo():
    if "user_id" not in session:
        return jsonify({'status': 'error', 'message': 'Please log in to delete a to-do.'}), 401

    task_id = request.form.get('task_id')
    task = db_session.query(Task).get(task_id)

    if task and task.user_id == session["user_id"]:
        db_session.delete(task)
        db_session.commit()
        return jsonify({'status': 'success', 'task_id': task_id})
    else:
        return jsonify({'status': 'error', 'message': 'To-Do not found or access denied'}), 400

@app.route('/update_task_status', methods=["POST"])
def update_task_status():
    if "user_id" not in session:
        return jsonify({'status': 'error', 'message': 'Please log in to update a task.'}), 401

    task_id = request.form.get('task_id')
    completed = request.form.get('completed') == 'true'

    task = db_session.query(Task).get(task_id)

    if task and task.user_id == session["user_id"]:
        task.completed = completed
        db_session.commit()
        return jsonify({'status': 'success', 'task_id': task_id, 'completed': completed})
    else:
        return jsonify({'status': 'error', 'message': 'To-Do not found or access denied'}), 400

@app.route('/update_task_due_date', methods=["POST"])
def update_task_due_date():
    if "user_id" not in session:
        return jsonify({'status': 'error', 'message': 'Please log in to update a task.'}), 401

    task_id = request.form.get('task_id')
    due_date_str = request.form.get('due_date')

    task = db_session.query(Task).get(task_id)

    if task and task.user_id == session["user_id"]:
        task.due_date = datetime.strptime(due_date_str, '%Y-%m-%d') if due_date_str else None
        db_session.commit()
        return jsonify({'status': 'success', 'task_id': task_id, 'due_date': task.due_date})
    else:
        return jsonify({'status': 'error', 'message': 'To-Do not found or access denied'}), 400

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

# Add favicon route
@app.route('/favicon.ico')
def favicon():
    return redirect(url_for('static', filename='img/favicon.ico'))

@app.context_processor
def inject_favicon():
    return dict(favicon_url=url_for('static', filename='img/favicon.ico'))

if __name__ == '__main__':
    app.run(debug=True)