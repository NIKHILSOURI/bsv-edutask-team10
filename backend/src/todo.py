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

    def get_todo(self, object_id):
        todo = self.collection.find_one({ '_id': ObjectId(object_id)})
        return self.to_json(todo)

    def get_todos_of_task(self, task_id: str):
        todos = self.collection.find({'task': ObjectId(task_id)})
        return list(todos)

    #def update(self):
    #    pass

    #def delete(self):
    #    pass

    def to_json(self, data):
        return json.loads(json_util.dumps(data))
