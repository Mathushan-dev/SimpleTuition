from pymongo import MongoClient
from pymongo.errors import PyMongoError
from datetime import datetime
import os

# Reads MONGODB_URI or DATABASE_URL, fall back to local dev instance
MONGODB_URI = os.environ.get("MONGODB_URI") or os.environ.get("DATABASE_URL") or "mongodb://localhost:27017"

client = None
db = None

def init_mongo():
    global client, db
    try:
        # Delay-construct client. Use certifi CA bundle when available
        kwargs = {}
        try:
            import certifi
            kwargs['tlsCAFile'] = certifi.where()
        except Exception:
            # certifi not available; fall back to system CA store
            pass
        client = MongoClient(MONGODB_URI, **kwargs)
        # Ping server
        client.admin.command('ping')
        # Default DB name: from URI or fallback
        default_db = os.environ.get('MONGODB_DB', 'tuition')
        db = client[default_db]
        # Ensure indexes for common collections
        users = db.get_collection('users')
        users.create_index('email', unique=True)
        users.create_index('user_id', unique=True)
        tokens = db.get_collection('reset_tokens')
        tokens.create_index('token', unique=True)
        bookings = db.get_collection('bookings')
        bookings.create_index('booking_id', unique=True)
        bookings.create_index('student_id')
        bookings.create_index('teacher_id')
        print("MongoDB initialized and connected to database:", default_db)
        return True
    except PyMongoError as e:
        print("Failed to initialize MongoDB:", e)
        client = None
        db = None
        return False


def serialize_booking(doc: dict):
    if not doc:
        return None
    out = {k: v for k, v in doc.items() if k != "_id"}
    dt = out.get("date_time")
    if isinstance(dt, str):
        try:
            out["date_time"] = datetime.fromisoformat(dt)
        except ValueError:
            pass
    return out

# --- Basic DAL helpers ---
def create_user(doc: dict):
    """Insert a user document and return inserted id or raise."""
    if db is None:
        raise RuntimeError("MongoDB not initialized")
    return db.users.insert_one(doc).inserted_id

def find_user_by_email(email: str):
    if db is None:
        return None
    return db.users.find_one({"email": email})

def find_user_by_id(user_id):
    if db is None:
        return None
    return db.users.find_one({"user_id": user_id})

def create_booking(doc: dict):
    if db is None:
        raise RuntimeError("MongoDB not initialized")
    return db.bookings.insert_one(doc).inserted_id

def get_bookings_for_user(user_id):
    if db is None:
        return []
    return list(db.bookings.find({"user_id": user_id}))

def create_reset_token(doc: dict):
    if db is None:
        raise RuntimeError("MongoDB not initialized")
    return db.reset_tokens.insert_one(doc).inserted_id

def find_reset_token(token: str):
    if db is None:
        return None
    return db.reset_tokens.find_one({"token": token})

def delete_reset_token(token: str):
    if db is None:
        return None
    return db.reset_tokens.delete_one({"token": token})


# --- Subject / Pricing / Payments helpers ---
def create_subject(doc: dict):
    """doc: {subject_id, name, description}
    """
    if db is None:
        raise RuntimeError("MongoDB not initialized")
    return db.subjects.insert_one(doc).inserted_id


def find_subject_by_id(subject_id):
    if db is None:
        return None
    return db.subjects.find_one({"subject_id": subject_id})


def list_subjects():
    if db is None:
        return []
    return list(db.subjects.find())


def assign_student_to_subject(doc: dict):
    """doc: {subject_id, student_id, price_override (optional)}"""
    if db is None:
        raise RuntimeError("MongoDB not initialized")
    return db.subject_assignments.insert_one(doc).inserted_id


def list_subject_assignments(subject_id=None):
    if db is None:
        return []
    q = {} if subject_id is None else {"subject_id": subject_id}
    return list(db.subject_assignments.find(q))


def set_student_price(subject_id, student_id, price):
    if db is None:
        raise RuntimeError("MongoDB not initialized")
    return db.subject_assignments.update_one({"subject_id": subject_id, "student_id": student_id}, {"$set": {"price": price}}, upsert=True)


def record_tutor_payment(doc: dict):
    """doc: {tutor_id, subject_id, amount, date, notes}"""
    if db is None:
        raise RuntimeError("MongoDB not initialized")
    return db.tutor_payments.insert_one(doc).inserted_id


def list_tutor_payments(tutor_id=None):
    if db is None:
        return []
    q = {} if tutor_id is None else {"tutor_id": tutor_id}
    return list(db.tutor_payments.find(q))


def serialize_user(doc: dict, include_password: bool = False):
    if not doc:
        return None
    out = {k: v for k, v in doc.items() if k != "_id"}
    if not include_password and "password" in out:
        out.pop("password")
    return out


def serialize_subject(doc: dict):
    if not doc:
        return None
    return {k: v for k, v in doc.items() if k != "_id"}
