from  src.util.dao import DAO

dao = DAO(collection_name='user')

# create a new user
def create_user(data):
    try:
        return dao.create(data)
    except Exception as e:
        raise

# get a user by id
def get_user(id):
    try:
        return dao.findOne(id)
    except Exception as e:
        raise

# get a user by his email
def get_user_by_email(email):
    try:
        if '@' not in email:
            raise ValueError('Error: invalid email address')

        users = dao.find({'email': email})
        if len(users) == 0:
            return None
        elif len(users) > 1:
            print(f'Error: more than one user found with mail {email}')
            return users[0]
        # exactly one user was found
        return users[0]
    except Exception as e:
        raise

# get all users
def get_all_users():
    try:
        return dao.find()
    except Exception as e:
        raise

# update a user
def update_user(id, data):
    try:
        #update_result = users_dao.update_user(id, data)
        update_result = dao.update(id=id, update_data={'$set': data})
        return update_result
    except Exception as e:
        raise