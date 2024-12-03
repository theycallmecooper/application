from flask import Flask, render_template, request, flash, session, redirect, url_for, jsonify
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Date
from datetime import datetime, timedelta
from setup_db import User, Task, Category  # Ensure User and Task models are defined in setup_db
import random

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
    tasks_with_time_remaining = []
    today = datetime.now().date()
    for task in tasks:
        if task.due_date:
            delta = task.due_date - today
            if delta.days > 0:
                badge_class = "badge-upcoming"
                badge_text = f"In {delta.days} day{'s' if delta.days != 1 else ''}"
                is_overdue = False
                is_due_today = False
            elif delta.days == 0:
                badge_class = "badge-due-today"
                badge_text = "Due today"
                is_overdue = False
                is_due_today = True
            else:
                badge_class = "badge-overdue"
                badge_text = f"Overdue by {abs(delta.days)} day{'s' if abs(delta.days) != 1 else ''}"
                is_overdue = True
                is_due_today = False
        else:
            badge_class = "badge-no-due"
            badge_text = "No due date"
            is_overdue = False
            is_due_today = False

        if task.completed:
            badge_class = "badge-completed"
            badge_text = "Completed"

        tasks_with_time_remaining.append({
            'id': task.id,
            'description': task.description,
            'due_date': task.due_date,
            'badge_class': badge_class,
            'badge_text': badge_text,
            'is_overdue': is_overdue,
            'is_due_today': is_due_today,
            'completed': task.completed,
            'category_id': task.category_id,
            'brief_description': task.brief_description
        })
    return render_template('dashboard.html', tasks=tasks_with_time_remaining, categories=categories, current_date=today)

@app.route('/add_todo', methods=["POST"])
def add_todo():
    if "user_id" not in session:
        flash("Please log in to add a to-do.", "warning")
        return redirect(url_for('login'))

    task_description = request.form.get("task")
    due_date_str = request.form.get("due_date")
    brief_description = request.form.get("task_description")
    if not task_description.strip():
        flash("Task description cannot be empty.", "warning")
        return redirect(url_for('dashboard'))

    user_id = session["user_id"]
    due_date = datetime.strptime(due_date_str, '%Y-%m-%d') if due_date_str else None
    category_id = request.form.get("category")
    category = db_session.query(Category).get(category_id) if category_id else None
    new_task = Task(description=task_description.strip(), user_id=user_id, completed=False, due_date=due_date, category=category, brief_description=brief_description)
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

@app.route('/delete_category', methods=["POST"])
def delete_category():
    if "user_id" not in session:
        flash("Please log in to delete a category.", "warning")
        return redirect(url_for('login'))

    category_id = request.form.get('category_id')
    category = db_session.query(Category).get(category_id)
    if category:
        db_session.delete(category)
        db_session.commit()
        flash("Category deleted successfully!", "success")
    else:
        flash("Category not found.", "error")
    return redirect(url_for('dashboard'))

@app.route('/calendar')
def calendar():
    if "user_id" not in session:
        flash("Please log in to view the calendar.", "warning")
        return redirect(url_for('login'))

    tasks = db_session.query(Task).filter_by(user_id=session['user_id']).all()
    tasks_with_time_remaining = []
    today = datetime.now().date()
    for task in tasks:
        if task.due_date:
            delta = task.due_date - today
            if delta.days > 0:
                time_remaining = f"In {delta.days} day{'s' if delta.days != 1 else ''}"
                is_overdue = False
                is_due_today = False
            elif delta.days == 0:
                time_remaining = "Due today"
                is_overdue = False
                is_due_today = True
            else:
                time_remaining = f"Overdue by {abs(delta.days)} day{'s' if abs(delta.days) != 1 else ''}"
                is_overdue = True
                is_due_today = False
        else:
            time_remaining = None
            is_overdue = False
            is_due_today = False
        tasks_with_time_remaining.append({
            'description': task.description,
            'due_date': task.due_date,
            'time_remaining': time_remaining,
            'is_overdue': is_overdue,
            'is_due_today': is_due_today
        })
    return render_template('calendar.html', tasks=tasks_with_time_remaining)

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/add_random_todo', methods=["POST"])
def add_random_todo():
    if "user_id" not in session:
        flash("Please log in to add a to-do.", "warning")
        return redirect(url_for('login'))

    random_todos = [
        "Give someone a hug",
        "Buy someone a coffee",
        "Compliment a stranger",
        "Write a thank you note",
        "Help someone with a task",
        "Donate to a charity",
        "Call a friend or family member",
        "Leave a positive review",
        "Pick up litter",
        "Smile at everyone you see"
    ]
    task_description = random.choice(random_todos)
    due_date = datetime.now().date() + timedelta(days=1)
    user_id = session["user_id"]

    # Assuming "Personal" category exists and has id 1
    category = db_session.query(Category).filter_by(name="Personal").first()
    if not category:
        flash("Personal category not found.", "error")
        return redirect(url_for('dashboard'))

    new_task = Task(description=task_description, user_id=user_id, completed=False, due_date=due_date, category=category)
    db_session.add(new_task)
    db_session.commit()

    flash("Random To-Do added successfully!", "success")
    return redirect(url_for('dashboard'))

@app.route('/edit_todo', methods=["POST"])
def edit_todo():
    if "user_id" not in session:
        flash("Please log in to edit a to-do.", "warning")
        return redirect(url_for('login'))

    task_id = request.form.get("task_id")
    task_description = request.form.get("task_description")
    due_date_str = request.form.get("due_date")
    category_id = request.form.get("category")
    brief_description = request.form.get("task_brief_description")

    task = db_session.query(Task).get(task_id)

    if task and task.user_id == session["user_id"]:
        task.description = task_description.strip()
        task.due_date = datetime.strptime(due_date_str, '%Y-%m-%d') if due_date_str else None
        task.category_id = category_id if category_id else None
        task.brief_description = brief_description
        db_session.commit()
        flash("To-Do updated successfully!", "success")
    else:
        flash("To-Do not found or access denied.", "error")

    return redirect(url_for('dashboard'))

# Add favicon route
@app.route('/favicon.ico')
def favicon():
    return redirect(url_for('static', filename='img/favicon.ico'))

@app.context_processor
def inject_favicon():
    return dict(favicon_url=url_for('static', filename='img/favicon.ico'))

if __name__ == '__main__':
    app.run(debug=True)