# coding=utf-8
import json
from bson import json_util
from bson.objectid import ObjectId


class Todo:

    def __init__(self, database):
        self.database = database
        self.collection = self.database.todo

    def create(self, data):
        todo = {
            'description': data.get('description'),
            'done': False,
            'task': ObjectId(data.get('taskid'))
        }

        inserted_id = self.collection.insert_one(todo).inserted_id
        todo = self.collection.find_one({ '_id': ObjectId(inserted_id) })
        
        return self.to_json(todo)

    # return all todo objects of a task
    def get_todos_of_task(self, task_id: str):
        todos = []
        try:
            todoobjects = self.collection.find({'task': ObjectId(task_id)})

            for obj in todoobjects:
                todos.append(self.to_json(obj))
        except Exception as e:
            print(e)
        finally:
            return todos

    def to_json(self, data):
        return json.loads(json_util.dumps(data))
