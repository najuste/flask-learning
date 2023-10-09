from flask import Flask, render_template, request, redirect, url_for, flash, jsonify

# flask needs to know where the project is. So the module name is this module title
app = Flask(__name__)
# needed for flash
app.secret_key = 'your_secret_key'

todo_list = ['Clean my desk', 'Schedule a photo shoot', 'Do a Python KATA']


@app.route('/', methods=['GET', 'POST'])
def index():
    global todo_list # define it is globally avail!
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


# api part
@app.route('/api/items')
def get_items():
    global todo_list
    return jsonify({'items': todo_list})


# run web server
# best practice so that app server is started only when you run this file as the main file
if __name__ == '__main__':
    app.run(debug=True)  # this would run a development server only
