import os
from datetime import datetime

# instantiate pymongo and create a connection to the database
import pymongo
client = pymongo.MongoClient(os.environ.get('MONGO_URL'))
database = client.todo_list

# create a data access object
from src.daos.task import Task
from src.daos.video import Video
from src.daos.todo import Todo
tasks_dao = Task(database)
videos_dao = Video(database)
todos_dao = Todo(database)

# create a new task
def create_task(data):
    # make sure all mandatory fields are set
    if not all (key in data for key in ('title', 'userid', 'url', 'todos')):
        return None

    # fill default values for missing values
    if 'startdate' not in data:
        data['startdate'] = datetime.today().strftime('%Y-%m-%d')
    if 'duedate' not in data:
        data['duedate'] = None
    if 'categories' not in data:
        data['categories'] = []

    # create the task object
    task = tasks_dao.create(data)

    # add the video url
    video = videos_dao.create({
        'url': data['url'],
        'taskid': task['_id']['$oid']
    })
    tasks_dao.add_video(task_id=task['_id']['$oid'], video_id=video['_id']['$oid'])

    # create and add todos
    for todo in data['todos']:
        todoobj = todos_dao.create({
            'description': todo,
            'taskid': task['_id']['$oid']
        })
        tasks_dao.add_todo(task_id=task['_id']['$oid'], todo_id=todoobj['_id']['$oid'])

    return task['_id']['$oid']

# get a task by id
def get_task(id):
    return tasks_dao.get_task(id)

# get all tasks of a user
def get_tasks_of_user(id):
    tasks = tasks_dao.get_tasks_of_user(id)

    for task in tasks:
        # populate the video of each task
        video = videos_dao.get_video(task['video']['$oid'])
        task['video'] = video['url']

        # populate the todos of each task
        todoobjs = todos_dao.get_todos_of_task(task['_id']['$oid'])
        todos = []
        for todo in todoobjs:
            todos.append({
                'description': todo['description'],
                'done': todo['done']
            })
        task['todos'] = todos
    
    return tasks