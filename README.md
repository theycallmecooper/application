<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Done'N'Dusted - README</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <style>
        body {
            font-family: Arial, sans-serif;
            padding: 20px;
        }
        h1, h2 {
            color: #221397;
        }
        .code-block {
            background-color: #f8f9fa;
            border: 1px solid #ddd;
            padding: 10px;
            border-radius: 5px;
            font-family: monospace;
        }
    </style>
</head>
<body>
    <h1>Done'N'Dusted</h1>
    <p>Done'N'Dusted is a personal task management web application designed to help you stay organized and productive. This application allows users to sign up, log in, manage tasks, and categorize them efficiently.</p>

    <h2>Features</h2>
    <ul>
        <li>User Authentication (Sign Up, Log In, Log Out)</li>
        <li>Task Management (Add, Delete, Mark as Completed)</li>
        <li>Category Management (Add, Delete)</li>
        <li>Task Due Date Tracking</li>
        <li>Responsive Design with Bootstrap</li>
        <li>Animated Backgrounds and UI Elements</li>
    </ul>

    <h2>Technologies Used</h2>
    <ul>
        <li>Flask (Python)</li>
        <li>SQLAlchemy (ORM)</li>
        <li>SQLite (Database)</li>
        <li>HTML, CSS, JavaScript</li>
        <li>Bootstrap (CSS Framework)</li>
        <li>jQuery (JavaScript Library)</li>
    </ul>

    <h2>Setup Instructions</h2>
    <ol>
        <li><strong>Clone the repository:</strong>
            <div class="code-block">
                <code>git clone https://github.com/yourusername/application.git<br>cd donendusted</code>
            </div>
        </li>
        <li><strong>Create a virtual environment and activate it:</strong>
            <div class="code-block">
                <code>python -m venv venv<br>source venv/bin/activate  # On Windows use `venv\Scripts\activate`</code>
            </div>
        </li>
        <li><strong>Install the required dependencies:</strong>
            <div class="code-block">
                <code>pip install -r requirements.txt</code>
            </div>
        </li>
        <li><strong>Set up the database:</strong>
            <div class="code-block">
                <code>python setup_db.py</code>
            </div>
        </li>
        <li><strong>Run the application:</strong>
            <div class="code-block">
                <code>python app.py</code>
            </div>
        </li>
        <li><strong>Open your web browser and navigate to:</strong>
            <div class="code-block">
                <code>http://127.0.0.1:5000</code>
            </div>
        </li>
    </ol>

    <h2>Usage</h2>
    <h3>Sign Up</h3>
    <p>Navigate to the Sign Up page. Enter a unique username and password. Click the "Sign Up" button.</p>

    <h3>Log In</h3>
    <p>Navigate to the Log In page. Enter your username and password. Click the "Login" button.</p>

    <h3>Dashboard</h3>
    <p>Add new tasks with optional due dates and categories. Mark tasks as completed by checking the checkbox. Delete tasks using the "Delete" button. Add or delete categories.</p>

    <h3>Calendar</h3>
    <p>View tasks with their due dates on a calendar.</p>

    <h2>Contributing</h2>
    <p>Contributions are welcome! Please fork the repository and create a pull request with your changes.</p>

    <h2>License</h2>
    <p>This project is licensed under the MIT License. See the <a href="LICENSE">LICENSE</a> file for details.</p>

    <h2>Acknowledgements</h2>
    <ul>
        <li><a href="https://flask.palletsprojects.com/">Flask</a></li>
        <li><a href="https://getbootstrap.com/">Bootstrap</a></li>
        <li><a href="https://jquery.com/">jQuery</a></li>
        <li><a href="https://fullcalendar.io/">FullCalendar</a></li>
    </ul>
</body>
</html>
