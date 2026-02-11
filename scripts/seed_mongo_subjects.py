#!/usr/bin/env python3
"""Seed sample subjects, assignments and tutor payments into MongoDB for testing.
Usage:
PYTHONPATH=. SSL_CERT_FILE=$(python3 -m certifi) MONGODB_URI="..." MONGODB_DB="tuition" python3 scripts/seed_mongo_subjects.py
"""
import os
from pymongo import MongoClient

MONGODB_URI = os.environ.get('MONGODB_URI') or os.environ.get('DATABASE_URL') or 'mongodb://localhost:27017'
MONGODB_DB = os.environ.get('MONGODB_DB', 'tuition')

if not MONGODB_URI:
    print('No MONGODB_URI provided')
    raise SystemExit(1)

client = MongoClient(MONGODB_URI)
db = client[MONGODB_DB]

subs = [
    {'subject_id': 1, 'name': 'Mathematics', 'description': 'KS3/GCSE/A-Level Maths'},
    {'subject_id': 2, 'name': 'Biology', 'description': 'KS3/GCSE Biology'},
    {'subject_id': 3, 'name': 'Chemistry', 'description': 'KS3/GCSE Chemistry'},
]
for s in subs:
    db.subjects.update_one({'subject_id': s['subject_id']}, {'$set': s}, upsert=True)

# assignments
assigns = [
    {'subject_id': 1, 'student_id': 101, 'price': 18},
    {'subject_id': 1, 'student_id': 102, 'price': 22},
    {'subject_id': 2, 'student_id': 103, 'price': 20},
]
for a in assigns:
    db.subject_assignments.update_one({'subject_id': a['subject_id'], 'student_id': a['student_id']}, {'$set': a}, upsert=True)

# tutor payments
payments = [
    {'tutor_id': 201, 'subject_id': 1, 'amount': 50, 'date': '2026-02-10', 'notes': 'Payout week 6'},
    {'tutor_id': 202, 'subject_id': 2, 'amount': 40, 'date': '2026-02-09', 'notes': 'Payout week 6'},
]
for p in payments:
    db.tutor_payments.insert_one(p)

print('Seed complete. Collections now:', db.list_collection_names())
print('Subjects:', list(db.subjects.find()))
print('Assignments:', list(db.subject_assignments.find()))
print('Tutor payments:', list(db.tutor_payments.find()))
