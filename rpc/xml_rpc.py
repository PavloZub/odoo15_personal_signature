import xmlrpc.client
from datetime import datetime

print('hello')
HOST = 'localhost'
PORT = 8569
DB = 'o15-learn1'
USER = 'admin'
PASS = 'admin'

root = 'http://%s:%d/xmlrpc/' % (HOST, PORT)
uid = xmlrpc.client.ServerProxy(root + 'common').login(DB, USER, PASS)
print("Logged in as %s (uid: %d)" % (USER, uid))

# read sessions
sessions = xmlrpc.client.ServerProxy(root + 'object').execute(DB, uid, PASS, 'open_academy.session',
                                                              'search_read', [], ['name','seats'])
for session in sessions:
    print("Session %s (%s seats)" % (session['name'], session['seats']))

# search session
course_id = xmlrpc.client.ServerProxy(root + 'object').execute(DB, uid, PASS, 'open_academy.course',
                                                                'search', [('name', 'ilike', 'FOB')])[0]
print('course_id', course_id)

# create a new session
session_id = xmlrpc.client.ServerProxy(root + 'object').execute(DB, uid, PASS, 'open_academy.session',
                                                                'create', {
            'name' : 'My session from console' + datetime.now().strftime("%H%M%S"),
            'course_id': course_id,
})
