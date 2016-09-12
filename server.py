import sqlite3
from flask import Flask, g, url_for, request, redirect, render_template

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


# Redirect to /list
@app.route('/', methods=['GET'])
def redirect_to_list():
    return redirect(url_for('list_stories'))


# helper function
def _get_data(id, db):
    titles = ('title', 'story', 'criteria',
                  'business_value', 'estimation', 'status')
    user_story = {}
    cur = db.execute("""SELECT title, story, criteria, business_value, estimation, status FROM user_stories WHERE id=?""", [id])
    try:
        story = cur.fetchall()[0]
        for i, title in enumerate(titles):
            print(story[i], title)
            user_story[title] = story[i]
        return user_story
    except IndexError:
        return user_story


# Edit story
@app.route('/story/<id>', methods=['GET'])
def editable_form(id):
    db = get_db()
    story = _get_data(id, db)
    return render_template('form.html', route='update_story', method='post',
                           title='Edit Story', button='Update', user_story=story, id=id,
                           statuses=('Planning', 'To Do', 'In Progress', 'Review', 'Done'))


@app.route('/update/<id>', methods=['POST'])
def update_story(id):
    db = get_db()
    db.execute("""UPDATE user_stories SET title=?, story=?, criteria=?, business_value=?, estimation=?, status=?
                  WHERE id=?""",
               [request.form['story_title'], request.form['story'],
                request.form['criteria'], request.form['business_value'],
                request.form['estimation'], request.form['status'], id])
    db.commit()
    return redirect(url_for('list_stories'))


# Add new story
@app.route('/story', methods=['GET'])
def blank_form():
    story = {}
    return render_template('form.html', route='new_story', method='post',
                           title='Add new Story', button='Create', user_story=story,
                           statuses=('Planning', 'To Do', 'In Progress', 'Review', 'Done'))


@app.route('/add', methods=['POST'])
def new_story():
    db = get_db()
    db.execute("""INSERT INTO user_stories (title, story, criteria, business_value, estimation, status)
               VALUES (?, ?, ?, ?, ?, ?)""",
               [request.form['story_title'], request.form['story'], request.form['criteria'],
                request.form['business_value'], request.form['estimation'], request.form['status']])
    db.commit()
    return redirect(url_for('list_stories'))


# List user stories
@app.route('/list', methods=['GET'])
def list_stories():
    db = get_db()
    query = """SELECT * FROM user_stories"""
    cur = db.execute(query)
    stories = cur.fetchall()
    return render_template('list.html', entries=stories)


# Delete story
@app.route('/del/<id>', methods=['POST'])
def delete_story(id):
    db = get_db()
    db.execute("""DELETE FROM user_stories WHERE id=?""", [id])
    db.commit()
    return redirect(url_for('list_stories'))

if __name__ == '__main__':
    app.run()