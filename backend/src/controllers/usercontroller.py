import os

# instantiate pymongo and create a connection to the database
import pymongo
client = pymongo.MongoClient(os.environ.get('MONGO_URL'))
database = client.todo_list

# create a data access object
from  src.daos.user import User
users_dao = User(database)

# create a new user
def create_user(data):
    if not all (key in data for key in ('firstName', 'lastName', 'email')):
        return None
        
    user = users_dao.create(data)
    if not user:
        return None
    return user

# get a user by id
def get_user(id):
    return users_dao.get_user_by_id(id)

# get all users
def get_all_users():
    return users_dao.get_all()

# update a user
def update_user(id, data):
    update_result = users_dao.update_user(id, data)
    return update_result