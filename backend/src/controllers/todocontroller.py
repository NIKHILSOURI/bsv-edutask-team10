from bson.objectid import ObjectId
from  src.util.dao import DAO

todos_dao = DAO(collection_name='todo')
tasks_dao = DAO(collection_name='task')

# create a new user
def create_todo(data):
    try:
        if 'taskid' in data:
            task = tasks_dao.findOne(id=data['taskid'])
            del data['taskid']

            todo = todos_dao.create(data)
            tasks_dao.update(id=task['_id']['$oid'], update_data={'$push' : {'todos': ObjectId(todo['_id']['$oid'])}})

            return todo
        else:
            return todos_dao.create(data)
    except Exception as e:
        raise

# get a user by id
def get_todo(id):
    try:
        return todos_dao.findOne(id)
    except Exception as e:
        raise

# update a user
def update_todo(id, data):
    try:
        #update_result = users_dao.update_user(id, data)
        update_result = todos_dao.update(id=id, update_data=data)
        return update_result
    except Exception as e:
        raise

def delete_todo(id):
    try:
        result = todos_dao.delete(id=id)
        return result
    except Exception as e:
        raise