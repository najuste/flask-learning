from flask import Blueprint, jsonify, abort, request
from db import engine as db
from models.tasks import Task


api_bp = Blueprint("api", __name__, url_prefix="/api")


@api_bp.route("/tasks", methods=["GET"])
def get_tasks():
    tasks = Task.query.limit(20).all()
    return jsonify({"tasks": tasks.to_dict()})


@api_bp.route("/tasks", methods=["POST"])
def add_task():
    if not request.json or "title" not in request.json:
        abort(400)
    task = Task(
        title=request.json["title"],
        created_by_id=request.json["created_by"],
    )
    db.session.add(task)
    db.session.commit()
    tasks = Task.query.limit(20).all()
    return jsonify({"tasks": tasks.to_dict()}, 21)


@api_bp.route("/tasks/<string:task>", methods=["GET"])
def get_task(task: str):
    task = Task.query.filter_by(title=task).first()
    if len(task) == 0:
        abort(404, "Item does not exist")
    return jsonify({"task": task})


@api_bp.route("/tasks/<string:task>", methods=["DELETE"])
def delete_task(task: str):
    task = Task.query.filter_by(title=task).first()
    if len(task) == 0:
        abort(404, "Item does not exist")
    db.session.delete(task)
    db.session.commit()
    return 200
