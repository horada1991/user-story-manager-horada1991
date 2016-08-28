import sqlite3
from flask import Flask, jsonify, g, current_app, request

app = Flask('User Story Manager')
DATABASE = 'user_story_manager.db'


# DB connect
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.teardown_appcontext
def close_db(exception):
    """Close the db at the end of the request"""
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def initdb():
    """Initializes the database."""
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    print('Initialized the database.')


# with app.app_context():
#     print(initdb())
#     print(current_app.name + ' started')