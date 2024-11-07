from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from setup_db import User, ToDo

#Connect to the database
engine = create_engine('sqlite:///todo.db')
Session = sessionmaker(bind=engine)
session = Session()

#Query all users and their tasks
users = session.query(User).all()
for user in users:
    print(f'User: {user.username}')
    for todo in user.todos:
        print(f' - Task: {todo.task}, Done: {todo.done}')