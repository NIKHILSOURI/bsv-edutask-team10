# coding=utf-8
import json
from bson import json_util
from bson.objectid import ObjectId

class User:

    def __init__(self, database):
        self.database = database
        self.user_collection = self.database.user

    # create a new user
    def create(self, data):
        # create a new user dict
        userdata = {
            'firstName': data.get('firstName'),
            'lastName': data.get('lastName'),
            'email': data.get('email'),
            'tasks': []
        }

        # insert 
        user = None
        try:
            inserted_id = self.user_collection.insert_one(userdata).inserted_id
            user = self.user_collection.find_one({ '_id': ObjectId(inserted_id) })
        except Exception as e:
            print(f'Error in User DAO: {e}')
        finally:
            if user != None:
                user = self.to_json(user)
            return user

    # obtain all users contained in the database
    def get_all(self):
        users = self.user_collection.find()
        return self.to_json(users)

    # obtain a single user entry by its id
    def get_user_by_id(self, object_id):
        user = None
        try:
            user = self.user_collection.find_one({ '_id': ObjectId(object_id)})
        except:
            print(f'Error: No user found with id {object_id}')
        finally:
            if user != None:
                user = self.to_json(user)
            return user

    # update a user
    def update_user(self, id, data): 
        success = False
        try:
            update_result = self.user_collection.update_one(
                {'_id': ObjectId(id)},
                {'$set': data}
            )
            success = update_result.acknowledged
        except Exception as e:
            print(e)
        finally:
            return success


    def add_task(self, user_id, task_id):
        self.user_collection.update_one(
            { '_id': ObjectId(user_id)}, 
            {'$push': {'tasks': ObjectId(task_id)}}
        )


    def to_json(self, data):
        return json.loads(json_util.dumps(data))
