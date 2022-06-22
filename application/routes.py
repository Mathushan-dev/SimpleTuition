from application import app
from flask import render_template, redirect, url_for, flash
from application.models import Questions, Users
from application.forms import RegisterForm, LoginForm, AnswerForm, AssignForm
from application import db
from flask_login import login_user, logout_user, login_required, current_user


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('index.html')


@app.route('/portal')
def portal_page():
    return render_template('portal.html')


@app.route('/assign', methods=['GET', 'POST'])
@login_required
def assign_page():
    if current_user.id == 1:
        form = AssignForm()
        if form.validate_on_submit():
            students = form.students.data
            homeworks = form.homeworks.data
            # attempted_user = Users.query.filter_by(username=form.username.data).first() if attempted_user and
            # attempted_user.check_password_correction( attempted_password=form.password.data ): login_user(
            # attempted_user) flash(f'Success! The homework has been assigned successfully: {
            # attempted_user.username}', category='success') return render_template('analyse.html') else: Ωflash(
            # 'Username and password are not match! Please try again', category='danger')
            flash(f"Temp {students} {homeworks}", category='success')
            return analyse_page()
        if form.errors != {}:  # If there are not errors from the validations
            for err_msg in form.errors.values():
                flash(f'There was an error with assigning the homework: {err_msg}', category='danger')

        return render_template('assign.html', form=form)

    return login_page()


@app.route('/analyse')
@login_required
def analyse_page():
    if current_user.id == 1:
        users = Users.query.all()
        return render_template('analyse.html', users=users)

    return login_page()


@app.route('/exam')
@login_required
def exam_page():
    if current_user.outstanding_questions is not None:
        outstanding_questions_list = current_user.outstanding_questions.split(",")
        questions = []

        for question_id in outstanding_questions_list:
            question = Questions.query.filter_by(id=question_id).first()
            questions.append(question)

        return render_template('exam.html', questions=questions)

    return render_template('wohoo.html')


@app.route('/attempt')
@login_required
def attempt_page():
    return render_template('attempt.html')


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = Users(username=form.username.data,
                               email_address=form.email_address.data,
                               password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f"Account created successfully! You are now logged in as {user_to_create.username}", category='success')
        return render_template('exam.html')
    if form.errors != {}:  # If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = Users.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
            return render_template('portal.html')
        else:
            flash('Username and password are not match! Please try again', category='danger')

    return render_template('login.html', form=form)


@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out!", category='info')
    return render_template('index.html')
