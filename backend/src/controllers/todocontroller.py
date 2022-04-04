from bson.objectid import ObjectId
from  src.util.dao import DAO

todos_dao = DAO(collection_name='todo')
tasks_dao = DAO(collection_name='task')

# create a new todo item
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

# get a todo item by id
def get_todo(id):
    try:
        return todos_dao.findOne(id)
    except Exception as e:
        raise

# update a todo item
def update_todo(id, data):
    try:
        update_result = todos_dao.update(id=id, update_data=data)
        return update_result
    except Exception as e:
        raise

# delete a todo utem
def delete_todo(id):
    try:
        result = todos_dao.delete(id=id)
        return result
    except Exception as e:
        raise