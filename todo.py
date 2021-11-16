# coding=utf-8
import json
from flask import Flask, jsonify, request, abort
from task import TaskDAO
import pymongo

app = Flask('todoapp')
client = pymongo.MongoClient('mongodb://localhost:27071')
database = client.todo_list
tasks_dao = TaskDAO(database)

@app.route('/')
def ping():
    return jsonify({'version': 1}), 200

@app.route('/tasks')
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
        data = request.json
        title = data.get('title', None)
        description = data.get('description', None)

        if not title or not description:
            return "The fields 'title' and 'description' are required", 400

        task = tasks_dao.create(data)

        return jsonify(task), 201


if __name__ == '__main__':
    app.run()
