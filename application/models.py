from application import db, login_manager
from application import bcrypt
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    outstanding_questions = db.Column(db.String(), nullable=False)
    completed_questions = db.Column(db.String(), nullable=False)
    log = db.Column(db.String(), nullable=False)

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)


class Questions(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    question = db.Column(db.String(length=100), nullable=False, unique=True)
    keywords = db.Column(db.String(length=150), nullable=False)
    exam_id = db.Column(db.Integer(), nullable=False)
