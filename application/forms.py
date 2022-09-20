from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectMultipleField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from wtforms.widgets import TextArea

from application.models import Questions, Users


def question_choices():
    questions = Questions.query.all()
    question_choices_list = []
    for question in questions:
        if question.id not in question_choices_list:
            question_choices_list.append(str(question.id) + " - " + question.question)

    return question_choices_list


def question_set_choices():
    questions = Questions.query.all()
    question_set_choices_list = []
    for question in questions:
        if question.exam_id not in question_set_choices_list:
            question_set_choices_list.append(str(question.exam_id))

    return question_set_choices_list


def student_choices():
    students = Users.query.all()
    student_choices_list = []
    for student in students:
        if student.id not in student_choices_list:
            student_choices_list.append(str(student.id) + " - " + student.username)

    return student_choices_list


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


class AnswerForm(FlaskForm):
    answer = StringField(label='Answer:', widget=TextArea(), validators=[DataRequired()],
                         render_kw={"rows": 10, "cols": 100})
    submit = SubmitField(label='Check Answer')
    report = SubmitField(label='Report (Enter your answer before reporting! No excuses!)')


class AttemptForm(FlaskForm):
    submit = SubmitField(label='Attempt')


class ClearForm(FlaskForm):
    submit = SubmitField(label='Clear')


class AssignForm(FlaskForm):
    students = SelectMultipleField(u'Student', choices=student_choices)
    questions = SelectMultipleField(u'Question', choices=question_choices)
    question_sets = SelectMultipleField(u'Question Set', choices=question_set_choices)
    submit = SubmitField(label='Assign Homework')
