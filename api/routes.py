from flask import Blueprint, jsonify, abort

api_bp = Blueprint("api", __name__, url_prefix="/api")

todo_list = ["Clean my desk", "Run", "Do a Python KATA"]


@api_bp.route("/tasks", methods=["GET"])
def get_tasks():
    global todo_list
    return jsonify({"tasks": todo_list})


@api_bp.route("/tasks/<string:task>", methods=["POST"])
def add_task(task: str):
    global todo_list
    todo_list.append(task)
    return jsonify({"tasks": todo_list})


@api_bp.route("/tasks/<string:task>", methods=["GET"])
def get_task(task: str):
    global todo_list
    task = [t for t in todo_list if t == task]
    if len(task) == 0:
        abort(404)
    return jsonify({"task": task})


@api_bp.route("/tasks/<string:task>", methods=["DELETE"])
def delete_task(task: str):
    global todo_list
    task = [t for t in todo_list if t == task]
    if len(task) == 0:
        abort(404, "Item does not exist")
    todo_list.remove(task[0])
    return jsonify({"tasks": todo_list})
