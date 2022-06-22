from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectMultipleField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from application.models import Users

studentIds = [('1', 'username1'), ('2', 'username2')]
questionSetIds = [('1', 'questionSet1'), ('2', 'questionSet2')]


class RegisterForm(FlaskForm):
    def validate_username(self, username_to_check):
        user = Users.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists! Please try a different username')

    def validate_email_address(self, email_address_to_check):
        email_address = Users.query.filter_by(email_address=email_address_to_check.data).first()
        if email_address:
            raise ValidationError('Email Address already exists! Please try a different email address')

    username = StringField(label='User Name:', validators=[Length(min=2, max=30), DataRequired()])
    email_address = StringField(label='Email Address:', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password:', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm Password:', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account')


class LoginForm(FlaskForm):
    username = StringField(label='User Name:', validators=[DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label='Sign in')


class AttemptForm(FlaskForm):
    answer = StringField(label='Answer:', validators=[DataRequired()])
    submit = SubmitField(label='Check Answer')


class AssignForm(FlaskForm):
    students = SelectMultipleField(u'Student', choices=studentIds)
    homeworks = SelectMultipleField(u'Question Set', choices=questionSetIds)
    submit = SubmitField(label='Assign Homework')