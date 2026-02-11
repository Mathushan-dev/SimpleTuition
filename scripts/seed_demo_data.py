#!/usr/bin/env python3
"""Seed demo data: tutors, students, subjects, and assignments.
Run with: MONGODB_URI='...' python3 scripts/seed_demo_data.py
"""
import os
import secrets
import bcrypt
from datetime import datetime
from pymongo import MongoClient

def get_client():
    uri = os.environ.get('MONGODB_URI') or os.environ.get('DATABASE_URL') or 'mongodb://localhost:27017'
    kwargs = {}
    try:
        import certifi
        kwargs['tlsCAFile'] = certifi.where()
    except Exception:
        pass
    return MongoClient(uri, **kwargs)

def next_user_id(db):
    cur = list(db.users.find({}, {'user_id':1}).sort('user_id', -1).limit(1))
    if cur and cur[0].get('user_id'):
        return cur[0]['user_id'] + 1
    return 1000

def hash_password(pw):
    return bcrypt.hashpw(pw.encode(), bcrypt.gensalt()).decode()

def main():
    client = get_client()
    dbname = os.environ.get('MONGODB_DB','tuition')
    db = client[dbname]

    print('Seeding demo data into', dbname)

    # create sample subjects
    subjects = [
        {'subject_id': 1, 'name': 'Mathematics', 'description': 'KS3/GCSE/A-Level maths tuition.'},
        {'subject_id': 2, 'name': 'Physics', 'description': 'Physics topics and exam technique.'},
        {'subject_id': 3, 'name': 'Chemistry', 'description': 'Chemistry lessons covering curricula.'},
    ]
    for s in subjects:
        db.subjects.update_one({'subject_id': s['subject_id']}, {'$set': s}, upsert=True)

    # create tutors
    tutors = [
        {'name':'Alice Tutor','email':'alice.tutor@example.com','user_type':'tutor'},
        {'name':'Bob Tutor','email':'bob.tutor@example.com','user_type':'tutor'},
    ]
    created_tutors = []
    for t in tutors:
        uid = next_user_id(db)
        pw = 'TutorPass' + secrets.token_urlsafe(6)
        doc = {'user_id': uid, 'name': t['name'], 'email': t['email'], 'password': hash_password(pw), 'user_type':'tutor', 'created_at': datetime.utcnow()}
        try:
            db.users.update_one({'email': t['email']}, {'$set': doc}, upsert=True)
        except Exception as e:
            print('Tutor upsert failed', e)
        created_tutors.append({'user_id': uid, 'email': t['email'], 'password': pw, 'name': t['name']})

    # create students
    students = [
        {'name':'Student One','email':'student.one@example.com','user_type':'student'},
        {'name':'Student Two','email':'student.two@example.com','user_type':'student'},
        {'name':'Student Three','email':'student.three@example.com','user_type':'student'},
    ]
    created_students = []
    for s in students:
        uid = next_user_id(db)
        pw = 'StudentPass' + secrets.token_urlsafe(6)
        doc = {'user_id': uid, 'name': s['name'], 'email': s['email'], 'password': hash_password(pw), 'user_type':'student','created_at': datetime.utcnow()}
        try:
            db.users.update_one({'email': s['email']}, {'$set': doc}, upsert=True)
        except Exception as e:
            print('Student upsert failed', e)
        created_students.append({'user_id': uid, 'email': s['email'], 'password': pw, 'name': s['name']})

    # create sample assignments (assign first two students to Mathematics, third to Physics)
    assigns = [
        {'subject_id':1, 'student_id': created_students[0]['user_id'], 'price': 22.5},
        {'subject_id':1, 'student_id': created_students[1]['user_id'], 'price': 18.0},
        {'subject_id':2, 'student_id': created_students[2]['user_id'], 'price': 20.0},
    ]
    for a in assigns:
        db.subject_assignments.update_one({'subject_id': a['subject_id'], 'student_id': a['student_id']}, {'$set': a}, upsert=True)

    print('\nCreated tutors:')
    for t in created_tutors:
        print(t)
    print('\nCreated students:')
    for s in created_students:
        print(s)

    print('\nSubjects and assignments seeded.')

if __name__ == '__main__':
    main()
