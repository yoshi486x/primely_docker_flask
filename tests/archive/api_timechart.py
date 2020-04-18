import json
import requests

# payloads = {'key1': 'value1', 'key2': 'value2'}
payloads = {'emp_no': 1614120}

def checker(response):
    print('status:', response.status_code)
    print('text:', response.text)
    print('json:', response.json)

r = requests.get("https://uu4cn1igsi.execute-api.us-east-1.amazonaws.com/dev", params=payloads)
# r = requests.get('https://uu4cn1igsi.execute-api.us-east-1.amazonaws.com/dev?emp_no=1614120')
# r = requests.get('http://httpbin.org/get', params=payloads)
# r.encoding = r.apparent_encoding
checker(r)
print(r.encoding)


# print(response)
# items = json.loads(response.text)
# print(items)


