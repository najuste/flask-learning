from flask import Blueprint, jsonify

api_bp = Blueprint('api', __name__, url_prefix='/api')

todo_list = ['Clean my desk', 'Schedule a photo shoot', 'Do a Python KATA']


@api_bp.route('/tasks', methods=['GET'])
def get_tasks():
    global todo_list
    return jsonify({'tasks': todo_list})