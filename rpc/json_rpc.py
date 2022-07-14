import json
import urllib.request
import random
from datetime import datetime

HOST = 'localhost'
PORT = 8569
DB = 'o15-learn1'
USER = 'admin'
PASS = 'admin'

root = 'http://%s:%d/jsonrpc' % (HOST, PORT)
service = "common"
method = "login"
args = [DB, USER, PASS]
params = {
    "service": service,
    "method": method,
    "args": args
}

data = {
    "jsonrpc": "2.0",
    "method": "call",
    "params": params,
    "id": random.randint(0, 1000000000)
}


req = urllib.request.Request(url=root, data=json.dumps(data).encode(), headers={
    "Content-Type": "application/json",
})
read = urllib.request.urlopen(req).read().decode('UTF-8')
# print(read)
reply = json.loads(read)
uid = reply['result']
print(reply)
print(uid)

service = "object"
method = "execute"
course_id = 15
args = [DB, uid, PASS, 'open_academy.session', 'create', {
            'name' : 'My session from console' + datetime.now().strftime("%H%M%S"),
            'course_id': course_id,}]
params = {
    "service": service,
    "method": method,
    "args": args
}
data = {
    "jsonrpc": "2.0",
    "method": "call",
    "params": params,
    "id": random.randint(0, 1000000000)
}
print(data)

req = urllib.request.Request(url=root, data=json.dumps(data).encode(), headers={
    "Content-Type": "application/json",
})
read = urllib.request.urlopen(req).read().decode('UTF-8')
reply = json.loads(read)
session_id = reply['result']
print(session_id)
