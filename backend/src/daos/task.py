# coding=utf-8
import json
from bson import json_util
from bson.objectid import ObjectId


class Task:
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
            'categories': data.get('categories'),
            'todos': [],
            'video': None
        }

        # store the task in the database
        inserted_id = self.collection.insert_one(task).inserted_id
        task = self.collection.find_one({ '_id': ObjectId(inserted_id) })

        return self.to_json(task)

    # obtain a task by its id
    def get_task(self, task_id: str):
        task = None
        try:
            task = self.collection.find_one({ '_id': ObjectId(task_id)})
        except Exception as e:
            print(e)
        finally:
            if task:
                task = self.to_json(task)
            return task

    # obtain all tasks associated to one user
    def get_tasks_of_user(self, user_id: str):
        tasks = []
        try:
            taskobjects = self.collection.find({'users': ObjectId(user_id)})

            for obj in taskobjects:
                tasks.append(self.to_json(obj))
        except Exception as e:
            print(e)
        finally:
            return tasks

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
