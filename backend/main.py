# coding=utf-8
from flask import Flask, jsonify, request, abort
from flask_cors import CORS, cross_origin
from src.task import TaskDAO
import pymongo

app = Flask('todoapp')
# configure CORS for cross-origin resource sharing (between the frontend and backend)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

client = pymongo.MongoClient('mongodb://localhost:27017')
database = client.todo_list
tasks_dao = TaskDAO(database)

@app.route('/')
def ping():
    return jsonify({'version': 1}), 200

@app.route('/tasks', methods=['GET'])
@cross_origin()
def list():
    print('retrieving tasks')
    return jsonify(tasks_dao.list()), 200


@app.route('/tasks/<pk>', methods=['GET', 'PUT'])
def get(pk):
    if request.method == 'GET':
        return jsonify(tasks_dao.read(pk))


@app.route('/tasks', methods=['POST'])
def create():
    if request.method == 'POST':
        # TODO json input forced - is this good?
        data = request.json
        title = data.get('title', None)
        description = data.get('description', None)

        if not title or not description:
            return "The fields 'title' and 'description' are required", 400

        task = tasks_dao.create(data)

        return jsonify(task), 201


if __name__ == '__main__':
    app.run()
