from flask import render_template
from app import app, db


@app.errorhandler(404)
def not_found_error(error):
    return render_template('error.html', error='404'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('error.html', error='500'), 500

# or, without the decorator
# app.register_error_handler(400, handle_bad_request) # function definition
