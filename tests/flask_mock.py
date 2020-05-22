import sqlite3

from flask import Flask
from flask import g
from flask import render_template
from flask import request
from flask import Response

DATABASE = 'test_sqlite.db'
app = Flask(__name__)


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/employee', methods=['POST', 'PUT', 'DELETE'])
@app.route('/employee/<name>', methods=['GET'])
def employee(name=None):
    db = get_db()
    curs = db.cursor()
    curs.execute(
        'CREATE TABLE IF NOT EXISTS persons( '
        'id INTEGER PRIMARY KEY AUTOINCREMENT, name STRING)'
    )

    name = request.values.get('name', name)
    if request.method == 'GET':
        # return name
        curs.execute('SELECT * FROM persons WHERE name = "{}"'. format(name))
        person = curs.fetchone()
        if not person:
            return "No", 404
        user_id, name = person
        return '{}:{}'.format(user_id, name), 200

    if request.method == 'POST':
        curs.execute('INSERT INTO persons(name) values("{}")'.format(name))
        db.commit()
        return 'created{}'.format(name), 201
    
    if request.method == 'PUT':
        new_name = request.values['new_name']
        curs.execute('UPDATE persons SET name = "{}" WHERE name = "{}"'.format(new_name, name))
        db.commit()
        return 'updated {}: {}'.format(name, new_name), 200

    if request.method == 'DELETE':
        curs.execute('DELETE from persons WHERE name = "{}"'.format(name))
        db.commit()
        return 'deleted {}'.format(name), 200



@app.route('/')
def hello_world():
    return 'top'

@app.route('/hello/')
@app.route('/hello/<username>')
def hello_world2(username=None):
    # return 'hello world! {}'.format(username)
    return render_template('hello.html', username=username)

@app.route('/post', methods=['POST', 'PUT', 'DELETE'])
def show_post():
    # return str(request.values)
    return str(request.values['username'])

def main():
    app.debug = True
    app.run()



if __name__ == "__main__":
    main()