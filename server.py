import sqlite3
from flask import Flask, g, url_for, request, flash, redirect

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


@app.route('/story', methods=['POST'])
def new_story():
    db = get_db()
    query = """INSERT INTO user_story_manager (title, story, criteria, business_value, estimation, status)
               VALUES (?, ?, ?, ?, ?, ?)""",\
            [request.form['title'], request.form['story'], request.form['criteria'],
             request.form['business_value'], request.form['estimation'], request.form['status']]

    db.execute(query)
    db.commit()
    flash('New story was successfully added')
    return redirect(url_for('list'))



# with app.app_context():
#     print(initdb())
#     print(current_app.name + ' started')
