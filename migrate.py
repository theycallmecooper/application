from sqlalchemy import create_engine, Column, Date, Integer, String, Table, MetaData, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base

# Connect to the database
engine = create_engine('sqlite:///todo.db')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

# Reflect the existing database
metadata = MetaData()

# Create categories table if it doesn't exist
categories_table = Table(
    'categories', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String, unique=True, nullable=False)
)
categories_table.create(engine, checkfirst=True)

# Reflect the tasks table
tasks_table = Table('tasks', metadata, autoload_with=engine)

# Add the new column
if not hasattr(tasks_table.c, 'due_date'):
    with engine.connect() as conn:
        conn.execute('ALTER TABLE tasks ADD COLUMN due_date DATE')

# Add category_id column to tasks table if it doesn't exist
if not hasattr(tasks_table.c, 'category_id'):
    category_id_column = Column('category_id', Integer, ForeignKey('categories.id'))
    category_id_column.create(tasks_table)

print("Database schema updated successfully.")