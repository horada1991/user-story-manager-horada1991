import sqlite3
from flask import Flask, g, url_for, request, flash, redirect, render_template

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


"""Edit a story"""
"""!!!!FINISH THIS!!!!"""
@app.route('/story/<story_id>', methods=['GET'])
def editable_form(story_id):
    pass


# Add new story
@app.route('/story', methods=['GET'])
def blank_form():
    return render_template('form.html', title='Add new Story')


@app.route('/story', methods=['POST'])
def new_story():
    db = get_db()
    db.execute("""INSERT INTO user_stories (title, story, criteria, business_value, estimation, status)
               VALUES (?, ?, ?, ?, ?, ?)""",
               [request.form['story_title'], request.form['story'], request.form['criteria'],
                request.form['business_value'], request.form['estimation'], request.form['status']])
    db.commit()
    return redirect(url_for('list_stories'))


"""List user stories"""


@app.route('/list', methods=['GET'])
def list_stories():
    db = get_db()
    query = """SELECT * FROM user_stories"""
    cur = db.execute(query)
    stories = cur.fetchall()
    return render_template('list.html', entries=stories)
