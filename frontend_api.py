import sqlite3

from flask import Flask
from flask import g
from flask import render_template
from flask import request
from flask import Response

# from primely.controller import controller
from primely.controller import controller

# DATABASE = 'test_sqlite.db'
app = Flask(__name__)


# def get_db():
#     db = getattr(g, '_database', None)
#     if db is None:
#         db = g._database = sqlite3.connect(DATABASE)
#     return db

# @app.teardown_appcontext
# def close_connection(exception):
#     db = getattr(g, '_database', None)
#     if db is not None:
#         db.close()

# @app.route('/app', methods=['POST', 'PUT', 'DELETE'])
# @app.route('/app/<name>', methods=['GET'])
# def employee(name=None):
#     db = get_db()
#     curs = db.cursor()
#     curs.execute(
#         'CREATE TABLE employees ('
#         'emp_no DECIMAL(7) PRIMARY KEY,'
#         'emp_name VARCHAR(100) NOT NULL,'
#         'dept_name VARCHAR(100));'
#     )

#     name = request.values.get('emp_no', emp_no)
#     if request.method == 'GET':
#         curs.execute('SELECT * FROM employees WHERE emp_no = "{}"'. format(emp_no))
#         employee = curs.fetchone()
#         if not employee:
#             return "No", 404
#         emp_no, emp_name, dept_name = employee
#         return '{}:{}:{}'.format(emp_no, emp_name, dept_name), 200

#     if request.method == 'POST':
#         curs.execute('INSERT INTO employees() values("{}")'.format(name))
#         db.commit()
#         return 'created{}'.format(name), 201



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

@app.route('/convert', methods=['GET'])
def run_conversion():
    if request.method == 'GET':
        conversion = controller.paycheck_analysis()
        if not conversion:
            return "No", 404

        return 'conversion success', 200

def main():
    app.debug = True
    app.run()



if __name__ == "__main__":
    main()