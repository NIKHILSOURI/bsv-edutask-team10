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
        #if 'duedate' not in data:
        #    data['duedate'] = None
        if 'categories' not in data:
            data['categories'] = []

        # add the video url
        video = videos_dao.create({'url': data['url'] })
        del data['url']
        data['video'] = ObjectId(video['_id']['$oid'])

        # create and add todos
        todos = []
        for todo in data['todos']:
            todoobj = todos_dao.create({'description': todo, 'done': False })
            todos.append(ObjectId(todoobj['_id']['$oid']))
        data['todos'] = todos
        
        # create the task object and assign it to the user
        task = tasks_dao.create(data)
        users_dao.update(uid, {'$push': {'tasks': ObjectId(task['_id']['$oid'])}})
        return task['_id']['$oid']
    except Exception as e:
        raise

# get a task by id
def get_task(id):
    try:
        return tasks_dao.findOne(id)
    except Exception as e:
        raise

# get all tasks of a user
def get_tasks_of_user(id):
    try:
        # get the user and the tasks associated to him
        user = users_dao.findOne(id)
        tasks = tasks_dao.find(filter={'_id': user['tasks']}, toid=['_id'])

        for task in tasks:
            # populate the video of each task
            video = videos_dao.findOne(task['video']['$oid'])
            task['video'] = video

            # populate the todos of each task
            todos = todos_dao.find(filter={'_id': task['todos']}, toid=['_id'])
            task['todos'] = todos
        
        return tasks
    except Exception as e:
        raise