from werkzeug.urls import urlsplit

from app import app
from flask import request, render_template, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user, login_required
from app.form import LoginForm
from app.models.users import User

todo_list = ['Clean my desk', 'Schedule a photo shoot', 'Do a Python KATA']


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
