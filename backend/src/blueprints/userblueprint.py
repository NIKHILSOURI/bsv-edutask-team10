from flask import Blueprint, jsonify, abort, request
from flask_cors import cross_origin

import src.controllers.usercontroller as controller

# instantiate the flask blueprint
user_blueprint = Blueprint('user_blueprint', __name__)

# create a new user
@user_blueprint.route('/create', methods=['POST'])
@cross_origin()
def create_user():
    data = request.form
    user = controller.create_user(data)
    if not user:
        abort(404)
    return jsonify(user)

# obtain one user by id (and optionally update him)
@user_blueprint.route('/<id>', methods=['GET', 'PUT'])
@cross_origin()
def get_user(id):
    # get a specific user
    if request.method == 'GET':
        user = controller.get_user(id)
        if not user:
            abort(404)
        return jsonify(user), 200
    # update the user
    elif request.method == 'PUT':
        data = request.form
        update_result = controller.update_user(id, data)
        if not update_result:
            return abort(404)
        user = controller.get_user(id)
        return jsonify(user), 200

# obtain all users and return them
@user_blueprint.route('/all', methods=['GET'])
@cross_origin()
def get_users():
    users = controller.get_all_users()
    return jsonify(users), 200