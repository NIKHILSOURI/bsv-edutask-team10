from bson.objectid import ObjectId
from datetime import datetime

# create a data access object
from src.util.dao import DAO
tasks_dao = DAO(collection_name='task')
videos_dao = DAO(collection_name='video')
todos_dao = DAO(collection_name='todo')
users_dao = DAO(collection_name='user')

# create a new task
def create_task(data):
    try:
        # store the user id
        uid = data['userid']
        del data['userid']

        # fill default values for missing values
        if 'startdate' not in data:
            data['startdate'] = datetime.today()
        if 'categories' not in data:
            data['categories'] = []

        # add the video url
        video = videos_dao.create({'url': data['url']})
        del data['url']
        data['video'] = ObjectId(video['_id']['$oid'])

        # create and add todos
        todos = []
        for todo in data['todos']:
            todoobj = todos_dao.create({'description': todo, 'done': False})
            todos.append(ObjectId(todoobj['_id']['$oid']))
        data['todos'] = todos

        # create the task object and assign it to the user
        task = tasks_dao.create(data)
        users_dao.update(
            uid, {'$push': {'tasks': ObjectId(task['_id']['$oid'])}})
        return task['_id']['$oid']
    except Exception as e:
        raise

# get a task by id
def get_task(id):
    try:
        # find the task
        task = tasks_dao.findOne(id)
        populate_task(task)
        return task
    except Exception as e:
        raise

# get all tasks of a user
def get_tasks_of_user(id):
    try:
        # get the user and the tasks associated to him
        user = users_dao.findOne(id)
        tasks = tasks_dao.find(filter={'_id': user['tasks']}, toid=['_id'])

        for task in tasks:
            populate_task(task)

        return tasks
    except Exception as e:
        raise

# helper method to populate the values of related elements
def populate_task(task):
    # populate the video of the task
    video = videos_dao.findOne(task['video']['$oid'])
    task['video'] = video

    # populate the todos of the task
    todos = todos_dao.find(filter={'_id': task['todos']}, toid=['_id'])
    task['todos'] = todos

# update a user
def update_task(id, data):
    try:
        #update_result = users_dao.update_user(id, data)
        update_result = tasks_dao.update(id=id, update_data=data)
        return tasks_dao.findOne(id)
    except Exception as e:
        raise
