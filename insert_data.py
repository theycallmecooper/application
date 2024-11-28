from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from werkzeug.security import generate_password_hash
from setup_db import User, Task, Category  # Ensure Category is imported

#connect to the database
engine = create_engine('sqlite:///todo.db')
Session = sessionmaker(bind=engine)
session = Session()

#Insert users with hashed passwords
user1 = User(username='john_doe', password=generate_password_hash('password123'))
user2 = User(username='jane_doe', password=generate_password_hash('password123'))

session.add(user1)
session.add(user2)
session.commit()

# Insert categories
category1 = Category(name='Work')
category2 = Category(name='Personal')
session.add_all([category1, category2])
session.commit()

# Insert tasks with categories
task1 = Task(description='Learn SQLAlchemy', completed=False, user_id=user1.id, category=category1)
task2 = Task(description='Build an app', completed=False, user_id=user2.id, category=category2)

session.add_all([task1, task2])
session.commit()

print("Users, categories, and tasks inserted successfully.")