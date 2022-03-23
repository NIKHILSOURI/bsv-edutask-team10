# coding=utf-8
from flask import Flask, jsonify, request, abort
from flask_cors import CORS, cross_origin

import pymongo
from src.user import User
from src.task import TaskDAO
from src.video import Video
from src.todo import Todo

app = Flask('todoapp')
# configure CORS for cross-origin resource sharing (between the frontend and backend)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# setup the database
client = pymongo.MongoClient('mongodb://localhost:27017')
database = client.todo_list
users_dao = User(database)
tasks_dao = TaskDAO(database)
video_dao = Video(database)
todo_dao = Todo(database)

@app.route('/')
def ping():
    return jsonify({'version': 1}), 200

# USERS
@app.route('/users', methods=['GET'])
@cross_origin()
def list_users():
    return jsonify(users_dao.list()), 200

# TASKS
@app.route('/tasks', methods=['GET'])
@cross_origin()
def list_tasks():
    return jsonify(tasks_dao.list()), 200

@app.route('/tasks/<fn>/<ln>', methods=['GET'])
@cross_origin()
def get_tasks_of_user(fn, ln):
    if request.method == 'GET':
        user = users_dao.get_user_by_name(firstname=fn, lastname=ln)
        
        tasks = []
        for taskoid in user['tasks']:
            task = tasks_dao.get_task(task_id=taskoid['$oid'])
            
            video = video_dao.get_video(object_id=task['video']['$oid'])
            task['video'] = video
            
            tasks.append(task)
        user['tasks'] = tasks

        return user


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

def populate(): 
    johndoe = users_dao.create({'firstName': 'John', 'lastName': 'Doe', 'email': 'john.doe@gmail.com'})

    # techstack video
    task_techstack = tasks_dao.create({'title': 'Tech Stacks', 'description': 'Understand the structure of a tech stack and explore popular stacks in use.', 'userid': johndoe['_id']['$oid']})
    users_dao.add_task(johndoe['_id']['$oid'], task_techstack['_id']['$oid'])

    video_techstack = video_dao.create({'url': 'Sxxw3qtb3_g', 'task': task_techstack['_id']['$oid']})
    tasks_dao.add_video(task_id=task_techstack['_id']['$oid'], video_id=video_techstack['_id']['$oid'])

    todo_techstack_watch = todo_dao.create({'description': 'Watch the video', 'task': task_techstack['_id']['$oid']})
    todo_techstack_implement = todo_dao.create({'description': 'Implement the techstack presented in the video', 'task': task_techstack['_id']['$oid']})

    tasks_dao.add_todo(task_id=task_techstack['_id']['$oid'], todo_id=todo_techstack_watch['_id']['$oid'])
    tasks_dao.add_todo(task_id=task_techstack['_id']['$oid'], todo_id=todo_techstack_implement['_id']['$oid'])

    # javascript pro tips video
    task_jspro = tasks_dao.create({'title': 'Javascript Pro Tips', 'description': 'Get better at writing JavaScript Code', 'userid': johndoe['_id']['$oid']})
    users_dao.add_task(johndoe['_id']['$oid'], task_jspro['_id']['$oid'])

    video_jspro = video_dao.create({'url': 'Mus_vwhTCq0', 'task': task_jspro['_id']['$oid']})
    tasks_dao.add_video(task_id=task_jspro['_id']['$oid'], video_id=video_jspro['_id']['$oid'])

if __name__ == '__main__':
    #populate()

    app.run()