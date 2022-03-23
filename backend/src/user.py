# coding=utf-8
import pymongo
import json
from bson import json_util
from bson.objectid import ObjectId


class User:

    def __init__(self, database):
        self.database = database
        self.user_collection = self.database.user

    def create(self, data):
        user = {
            'firstName': data.get('firstName'),
            'lastName': data.get('lastName'),
            'email': data.get('email'),
            'tasks': []
        }

        inserted_id = self.user_collection.insert_one(user).inserted_id
        user = self.user_collection.find_one({ '_id': ObjectId(inserted_id) })
        
        return self.to_json(user)

    def list(self):
        users = self.user_collection.find()
        return self.to_json(users)

    def get_user_by_id(self, object_id):
        user = self.user_collection.find_one({ '_id': ObjectId(object_id)})
        return self.to_json(user)

    def get_user_by_name(self, firstname: str, lastname: str):
        user = self.user_collection.find_one({'firstName': firstname, 'lastName': lastname})
        return self.to_json(user)

    def add_task(self, user_id, task_id):
        self.user_collection.update_one(
            { '_id': ObjectId(user_id)}, 
            {'$push': {'tasks': ObjectId(task_id)}}
        )

    #def update(self):
    #    pass

    #def delete(self):
    #    pass

    def to_json(self, data):
        return json.loads(json_util.dumps(data))
