from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user, login_required
import json
from werkzeug.urls import urlsplit
from datetime import datetime

from config import AppConfig
from models.users import User
from models.tasks import Task

from db import engine as db
from app.request_handling import RequestMethod, request_handling
from app.forms import LoginForm, RegistrationForm
from app import app

main_bp = Blueprint("main", __name__)


def get_global_todo():
    url = f"{AppConfig.API}/tasks"
    return request_handling(RequestMethod.GET, url, timeout=5)


def add_to_global_todo(request_data):
    print("add_to_global_todo")

    url = f"{AppConfig.API}/tasks"
    task = {
        "title": request_data["title"],
        "created_by": current_user.get_id(),
    }
    print("task", task)
    return request_handling(RequestMethod.POST, url, json=task)


def remove_from_todo(item: str):
    url = f"{AppConfig.API}/tasks/{item}"
    return request_handling(RequestMethod.DELETE, url)


@main_bp.before_request  # decorator func executed before the view function
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@main_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    form = LoginForm()
    if (
        form.validate_on_submit()
    ):  # GET will return false, so no need to check request method type
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.is_password_correct(form.password.data):
            login_user(
                user, remember=form.remember_me.data
            )  # it log-ins user and sets it  to the current_user
            next_page = request.args.get(
                "next"
            )  # the @login-required provides query param to use for redirect
            if (
                not next_page or urlsplit(next_page).netloc != ""
            ):  # if location is not relative redirect to index only
                next_page = url_for("main.index")
            return redirect(next_page)
        else:
            flash("Invalid user name or password")
            return redirect(url_for("main.login"))
    else:
        if request.method == "POST":
            flash("Form validation error", "error")
    return render_template("login.html", title="Sign In", form=form)


@main_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Congratulations, you are now a registered user!")
        return redirect(url_for("main.login"))
    return render_template("register.html", title="Register", form=form)


@main_bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.index"))


@main_bp.route("/", methods=["GET", "POST"])
def index():
    todo = []
    if request.method == "POST":
        response = add_to_global_todo(request.json)
        if response.success:
            todo = response.data["tasks"]
    else:
        todo_response = get_global_todo()
        if todo_response.success:
            todo = todo_response.data["tasks"]
    return render_template("main.html", items=todo)


@main_bp.route("/user/<username>")
@login_required
def user(username):
    given_user = User.query.filter_by(username=username).first_or_404()
    todo_list = [
        {"author": given_user, "task": "Todo #1"},
        {"author": given_user, "task": "Todo #2"},
    ]
    todo_items = [item["task"] for item in todo_list]
    return render_template("user.html", user=given_user, items=todo_items)


@main_bp.route("/remove/<item>")
# @login_required
def remove_item(item):
    remove_from_todo(item)
    return redirect(url_for("main.index"))
