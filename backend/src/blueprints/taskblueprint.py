from flask import Blueprint, jsonify, abort, request
from flask_cors import cross_origin

from pymongo.errors import WriteError

import src.controllers.taskcontroller as controller

# instantiate the flask blueprint
task_blueprint = Blueprint('task_blueprint', __name__)

# create a new task
@task_blueprint.route('/create', methods=['POST'])
@cross_origin()
def create():
    try:
        data = request.form.to_dict(flat=False)
        # convert all non-array fields back to simple values
        for key in ['title', 'description', 'start', 'due', 'userid', 'url']:
            if key in data and isinstance(data[key], list):
                data[key] = data[key][0]

        taskid = controller.create_task(data)
        return jsonify({'created': taskid}), 201
    except WriteError as e:
        abort(400, 'Invalid input data')
    except Exception as e:
        print(f'{e.__class__.__name__}: {e}')
        abort(500, 'Unknown server error')

# get or update a specific task
@task_blueprint.route('/byid/<id>', methods=['GET', 'PUT'])
@cross_origin()
def get(id):
    if request.method == 'GET':
        try:
            task = controller.get_task(id)
            return jsonify(task), 200
        except Exception as e:
            print(f'{e.__class__.__name__}: {e}')
            abort(500, 'Unknown server error')
    elif request.method == 'PUT':
        abort(501)

# obtain all tasks associated to a specific user
@task_blueprint.route('/ofuser/<id>', methods=['GET'])
@cross_origin()
def get_tasks_of_user(id):
    try:
        tasks = controller.get_tasks_of_user(id)
        return jsonify(tasks), 200
    except Exception as e:
        print(f'{e.__class__.__name__}: {e}')
        abort(500, 'Unknown server error')