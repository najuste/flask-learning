from app import app
from flask import request, render_template, redirect, url_for, flash


# needed for flash
app.secret_key = 'your_secret_key'
todo_list = ['Clean my desk', 'Schedule a photo shoot', 'Do a Python KATA']


@app.route('/', methods=['GET', 'POST'])
def index():
    global todo_list  # define it is globally avail!
    if request.method == 'POST':
        todo_list.append(request.form['item'])
    return render_template('index.html', items=todo_list)


@app.route('/remove/<item>')
def remove_item(item):
    global todo_list
    if item in todo_list:
        todo_list.remove(item)
    else:
        flash('Item does not exist.', 'error')
        return redirect(url_for('index'))
    return redirect(url_for('index'))  # func name index
