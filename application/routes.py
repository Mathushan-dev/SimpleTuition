from application import app
from flask import render_template, redirect, url_for, flash, request, session
from application.models import Questions, Users
from application.forms import RegisterForm, LoginForm, AttemptForm, AnswerForm, AssignForm, ClearForm
from application import db
from flask_login import login_user, logout_user, login_required, current_user
from application.questionMarker import analyse_answers
from datetime import datetime
import ast


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
            questions = form.questions.data
            question_sets = form.question_sets.data

            if students is not None and (questions is not None or question_sets is not None):
                questions_to_assign_list = []

                for question in questions:
                    if question.split("-")[0].strip() not in questions_to_assign_list:
                        questions_to_assign_list.append(question.split("-")[0].strip())

                for question_set in question_sets:
                    questions_to_append = Questions.query.filter_by(exam_id=question_set).all()
                    for question in questions_to_append:
                        if str(question.id) not in questions_to_assign_list:
                            questions_to_assign_list.append(str(question.id))

                for student in students:
                    student_to_assign = student.split("-")[0].strip()

                    if student_to_assign is not None:
                        student = Users.query.filter_by(id=student_to_assign).first()

                        if student is not None:
                            if student.outstanding_questions is not None:
                                temp_question_list = student.outstanding_questions.split(",")

                                for question in questions_to_assign_list:
                                    temp_question_list.append(question)
                                student.outstanding_questions = ",".join(list(dict.fromkeys(temp_question_list)))
                            else:
                                student.outstanding_questions = ",".join(questions_to_assign_list)

                            db.session.commit()

            return redirect(url_for('analyse_page'))

        if form.errors != {}:
            for err_msg in form.errors.values():
                flash(f'There was an error with assigning the homework: {err_msg}', category='danger')

        return render_template('assign.html', form=form)

    return login_page()


@app.route('/analyse', methods=['GET', 'POST'])
@login_required
def analyse_page():
    if current_user.id == 1:
        form = ClearForm()

        if form.validate_on_submit():
            user_id = request.form.get('user_id')
            user = Users.query.filter_by(id=user_id).first()
            user.log = "Cleared"
            db.session.commit()

            flash(f'{user.username}\'s log was cleared successfully.', category='success')
            return redirect(url_for('analyse_page'))

        if form.errors != {}:
            for err_msg in form.errors.values():
                flash(f'There was an error with clearing the log: {err_msg}', category='danger')

        users = Users.query.all()
        return render_template('analyse.html', users=users, form=form)

    return login_page()


@app.route('/exam', methods=['GET', 'POST'])
@login_required
def exam_page():
    if current_user.outstanding_questions is not None:
        form = AttemptForm()

        if form.validate_on_submit():
            session['question'] = request.form.get('question')
            session['question_id'] = request.form.get('question_id')
            return redirect(url_for('attempt_page'))

        if form.errors != {}:  # If there are errors from the validations
            for err_msg in form.errors.values():
                flash(f'There was an error with answering the homework: {err_msg}', category='danger')

        outstanding_questions_list = current_user.outstanding_questions.split(",")
        questions = []

        for question_id in outstanding_questions_list:
            question = Questions.query.filter_by(id=question_id).first()
            questions.append(question)

        return render_template('exam.html', questions=questions, form=form)

    return render_template('wohoo.html')


@app.route('/attempt', methods=['GET', 'POST'])
@login_required
def attempt_page():
    if current_user.id != 1:
        form = AnswerForm()

        if form.validate_on_submit():
            answer = form.answer.data.strip()
            question_id = request.form.get('question_id').strip()

            if form.report.data:
                now = datetime.now()
                timestamp = now.strftime("%m/%d/%Y, %H:%M:%S")
                current_user_log = current_user.log
                current_user.log = str(current_user_log) + "\n" + timestamp + ": \nQID-" + question_id + ", A-" + answer + "\n"
                db.session.commit()

            question = Questions.query.filter_by(id=question_id).first()
            actual_marks, maximum_marks, correct_answers = analyse_answers(answer.lower(), ast.literal_eval(question.keywords.lower()))

            if actual_marks == maximum_marks:
                flash(f'You have scored full marks on this question', category='success')

                if current_user.outstanding_questions is not None:
                    outstanding_questions_list = str(current_user.outstanding_questions).split(",")
                    new_outstanding_questions_list = []

                    for outstanding_question_id in outstanding_questions_list:
                        if outstanding_question_id != question_id:
                            new_outstanding_questions_list.append(outstanding_question_id)

                    if new_outstanding_questions_list:
                        current_user.outstanding_questions = ",".join(new_outstanding_questions_list)
                    else:
                        current_user.outstanding_questions = None
                    db.session.commit()

                if current_user.completed_questions is not None:
                    completed_questions_list = str(current_user.completed_questions).split(",")
                else:
                    completed_questions_list = []

                if question_id not in completed_questions_list:
                    completed_questions_list.append(question_id)
                current_user.completed_questions = ",".join(completed_questions_list)
                db.session.commit()

                return redirect(url_for('exam_page'))

            flash(f'You have scored {actual_marks} out of {maximum_marks} on this question', category='danger')
            flash(f'You have scored marks for the following sentences:\n {correct_answers}', category='success')

        if form.errors != {}:
            for err_msg in form.errors.values():
                flash(f'There was an error with answering the homework: {err_msg}', category='danger')

        return render_template('attempt.html', form=form, question=session['question'],
                               question_id=session['question_id'])

    return login_page()


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        now = datetime.now()
        timestamp = "Account created on " + now.strftime("%m/%d/%Y, %H:%M:%S")
        user_to_create = Users(username=form.username.data,
                               email_address=form.email_address.data,
                               password=form.password1.data,
                               log=timestamp)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f"Account created successfully! You are now logged in as {user_to_create.username}", category='success')
        return render_template('exam.html')

    if form.errors != {}:
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
