import json
import random
import requests
from datetime import datetime

HOST = 'localhost'
PORT = 8569
DB = 'o15-learn1'
USER = 'admin'
PASS = 'admin'

root = 'http://%s:%d/jsonrpc' % (HOST, PORT)
headers = {"Content-Type": "application/json"}

#content post request
def get_json_payload(service, method, *args):
    return json.dumps({
        "jsonrpc": "2.0",
        "method": 'call',
        "params": {
            "service": service,
            "method": method,
            "args": args
        },
        "id": random.randint(0, 100000000),
    })


payload = get_json_payload("common", "login", DB, USER, PASS)
print(type(payload))
response = requests.post(root, data=payload, headers=headers)
user_id = response.json()["result"]

if user_id:
    print("Success: User Id is ", user_id)
    search_domain = [['name', 'ilike', 'FOB']]
    payload = get_json_payload("object", "execute_kw", DB, user_id, PASS, 'open_academy.course',
                               'search', [search_domain])
    res = requests.post(root, data=payload, headers=headers).json()['result']
    print(res)

    #read data for courses ids
    payload = get_json_payload("object", "execute_kw", DB, user_id, PASS, 'open_academy.course',
                               'read', [res,['name', 'title', 'description']])
    res = requests.post(root, data=payload, headers=headers).json()['result']
    print(res)

    #create sessions
    create_sessions = [
        {'name': 'My session from console 1' + datetime.now().strftime("%H%M%S"),
         'course_id': 15},
        {'name': 'My session from console 2' + datetime.now().strftime("%H%M%S"),
         'course_id': 15}
    ]
    payload = get_json_payload("object", "execute_kw", DB, user_id, PASS, 'open_academy.session',
                               'create', [create_sessions])
    res = requests.post(root, data=payload, headers=headers).json()
    print(res)
else:
    print("Failed: wrong credentials")
