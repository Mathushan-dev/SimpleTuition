#!/usr/bin/env python3
"""Create an admin user in MongoDB if none exists and print credentials.
Usage:
PYTHONPATH=. SSL_CERT_FILE=$(python3 -m certifi) MONGODB_URI="..." MONGODB_DB="tuition" python3 scripts/create_admin.py
"""
import os
from pymongo import MongoClient
import bcrypt

MONGODB_URI = os.environ.get('MONGODB_URI') or os.environ.get('DATABASE_URL') or 'mongodb://localhost:27017'
MONGODB_DB = os.environ.get('MONGODB_DB', 'tuition')

if not MONGODB_URI:
    print('No MONGODB_URI provided')
    raise SystemExit(1)

c = MongoClient(MONGODB_URI)
db = c[MONGODB_DB]

admins = list(db.users.find({'user_type': 'admin'}))
if admins:
    for a in admins:
        print('EXISTING_ADMIN', a.get('user_id'), a.get('email'))
else:
    cur = list(db.users.find({}, {'user_id': 1}).sort('user_id', -1).limit(1))
    if cur:
        nid = (cur[0].get('user_id') or 0) + 1
    else:
        nid = 1000
    email = 'admin@simpletuition.local'
    password_plain = 'AdminPass123!'
    hashed = bcrypt.hashpw(password_plain.encode(), bcrypt.gensalt())
    doc = {'user_id': nid, 'name': 'Administrator', 'email': email, 'password': hashed.decode(), 'user_type': 'admin'}
    db.users.insert_one(doc)
    print('CREATED_ADMIN', nid, email, password_plain)
