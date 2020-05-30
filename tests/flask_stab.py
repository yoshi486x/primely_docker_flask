import requests

from context import flask_app


r = requests.delete(
    'http://127.0.0.1:5000/api/delete')
print(r.text)

# r = requests.post(
#     'http://127.0.0.1:5000/employee', data={'name': 'mike'})
# print(r.text)

# r = requests.put(
#     'http://127.0.0.1:5000/employee', data={'name': 'mike', 'new_name': 'sakai'})
# print(r.text)

# r = requests.delete(
#     'http://127.0.0.1:5000/employee', data={'name': 'mike'})
# print(r.text)