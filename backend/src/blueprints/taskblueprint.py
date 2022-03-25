from flask import Blueprint, jsonify, abort, request
from flask_cors import cross_origin

import src.controllers.taskcontroller as controller

# instantiate the flask blueprint
task_blueprint = Blueprint('task_blueprint', __name__)

# create a new task
@task_blueprint.route('/create', methods=['POST'])
@cross_origin()
def create():
    data = request.form.to_dict(flat=False)
    # convert all non-array fields back to simple values
    for key in ['title', 'description', 'start', 'due', 'userid', 'url']:
        if key in data and isinstance(data[key], list):
            data[key] = data[key][0]

    taskid = controller.create_task(data)
    if not taskid:
        abort(404)
    return jsonify({'created': taskid}), 201

# get or update a specific task
@task_blueprint.route('/byid/<id>', methods=['GET', 'PUT'])
@cross_origin()
def get(id):
    if request.method == 'GET':
        task = controller.get_task(id)
        if not task:
            abort(404)
        return jsonify(task), 200
    elif request.method == 'PUT':
        abort(501)

# obtain all tasks associated to a specific user
@task_blueprint.route('/ofuser/<id>', methods=['GET'])
@cross_origin()
def get_tasks_of_user(id):
    tasks = controller.get_tasks_of_user(id)
    return jsonify(tasks), 200