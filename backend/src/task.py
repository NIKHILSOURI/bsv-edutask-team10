# coding=utf-8
import json
from bson import json_util
from bson.objectid import ObjectId


class TaskDAO:
    def __init__(self, database):
        self.database = database
        self.collection = self.database.task

    def create(self, data):
        # create the task
        task = {
            'title': data.get('title'),
            'description': data.get('description'),
            'start': data.get('startdate'),
            'due': data.get('duedate'),
            'users': [ObjectId(data.get('userid'))],
            'requires': [],
            'category': None,
            'todos': [],
            'video': None
        }

        # store the task in the database
        inserted_id = self.collection.insert_one(task).inserted_id
        task = self.collection.find_one({ '_id': ObjectId(inserted_id) })

        return self.to_json(task)

    def get_all(self):
        tasks = self.collection.find()
        return self.to_json(tasks)

    def get_task(self, task_id: str):
        task = self.collection.find_one({ '_id': ObjectId(task_id)})
        return self.to_json(task)

    def get_tasks_of_user(self, user_id: str):
        tasks = self.collection.find({'users': ObjectId(user_id)})
        return list(tasks)

    def add_video(self, task_id: str, video_id: str):
        self.collection.update_one(
            { '_id': ObjectId(task_id)}, 
            {'$set': {'video': ObjectId(video_id)}}
        )

    def add_todo(self, task_id: str, todo_id: str):
        self.collection.update_one(
            { '_id': ObjectId(task_id)}, 
            {'$push': {'todos': ObjectId(todo_id)}}
        )

    def update(self):
        pass

    def delete(self):
        pass

    def to_json(self, data):
        return json.loads(json_util.dumps(data))
