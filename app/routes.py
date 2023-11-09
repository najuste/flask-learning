from app import app, db
from flask import request, render_template, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import urlsplit
from datetime import datetime

from app.forms import LoginForm, RegistrationForm
from app.models.users import User

todo_list = ['Clean my desk', 'Schedule a photo shoot', 'Do a Python KATA']

@app.before_request # decorator func executed right before the view function
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():  # on GET this will return false, so no need to check request method type
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.is_password_correct(form.password.data):
            login_user(user, remember=form.remember_me.data)  # it log-ins user and sets it  to the current_user
            next_page = request.args.get('next') # the @login-required provides next query param to use for redirect
            if not next_page or urlsplit(next_page).netloc != '': # if location is not relative redirect to index only
                next_page = url_for('index')
            return redirect(next_page)
        else:
            flash('Invalid user name or password')
            return redirect(url_for('login'))
    else:
        if request.method == 'POST':
            flash('Form validation error', 'error')
    return render_template('login.html', title='Sign In', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)



@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/', methods=['GET', 'POST'])
@login_required # this will redirect with query params
def index():
    global todo_list  # define it is globally avail!
    if request.method == 'POST':
        todo_list.append(request.form['item'])
    return render_template('main.html', items=todo_list)


@app.route('/user/<username>')
@login_required
def user(username):
    given_user = User.query.filter_by(username=username).first_or_404()
    todo_list = [
        {'author': given_user, 'task': 'Todo #1'},
        {'author': given_user, 'task': 'Todo #2'}
    ]
    todo_items=[item['task'] for item in todo_list]
    return render_template('user.html', user=given_user, items=todo_items)


@app.route('/remove/<item>')
@login_required
def remove_item(item):
    global todo_list
    if item in todo_list:
        todo_list.remove(item)
    else:
        flash('Item does not exist.', 'error')
        return redirect(url_for('index'))
    return redirect(url_for('index'))  # func name index
