from flask import Flask
from werkzeug.security import generate_password_hash
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from setup_db import User #import the user model from the models file.

app = Flask(__name__)
app.secret_key = '#sigmarizz23#'

#setup the database engine and session
engine = create_engine('sqlite:///todo.db')
Session = sessionmaker(bind=engine)
db_session = Session()

#define user details
username = "coopert"
password = "#fr33key"

#hash the password
hashed_password = generate_password_hash(password)

#check if the user already exists
existing_user = db_session.query(User).filter_by(username=username).first()
if existing_user:
	print(f"User '{username}' already exists.")
else:
	#create a new user instance
	new_user = User(username=username, password=hashed_password)

	#add user to the database
	db_session.add(new_user)
	db_session.commit()
	print(f"User '{username}' successfully added.")
