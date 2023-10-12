from app import app
from flask import request, render_template, redirect, url_for, flash

from app.form import LoginForm

todo_list = ['Clean my desk', 'Schedule a photo shoot', 'Do a Python KATA']


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit(): # on GET this will return false, so no need to check request method type
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    else:
        if request.method == 'POST':
            flash('Form validation error', 'error')
    return render_template('login.html', title='Sign In', form=form)


@app.route('/', methods=['GET', 'POST'])
def index():
    global todo_list  # define it is globally avail!
    if request.method == 'POST':
        todo_list.append(request.form['item'])
    return render_template('main.html', items=todo_list)


@app.route('/remove/<item>')
def remove_item(item):
    global todo_list
    if item in todo_list:
        todo_list.remove(item)
    else:
        flash('Item does not exist.', 'error')
        return redirect(url_for('index'))
    return redirect(url_for('index'))  # func name index
