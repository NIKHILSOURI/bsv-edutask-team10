# coding=utf-8
import os

from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin

app = Flask('todoapp')

# configure CORS for cross-origin resource sharing (between the frontend and backend)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# register blueprints
from src.blueprints.userblueprint import user_blueprint
from src.blueprints.taskblueprint import task_blueprint
app.register_blueprint(blueprint=user_blueprint, url_prefix='/users')
app.register_blueprint(blueprint=task_blueprint, url_prefix='/tasks')

import src.controllers.usercontroller as usercont
import src.controllers.taskcontroller as taskcont

@app.route('/')
@cross_origin()
def ping():
    return jsonify({'version': os.environ.get('VERSION')}), 200

@app.route('/populate', methods=['POST'])
@cross_origin()
def populate():
    janedoe = usercont.create_user({'firstName': 'Jane', 'lastName': 'Doe', 'email': 'jane.doe@gmail.com'})
    taskcont.create_task({
        'userid': janedoe['_id']['$oid'],
        'title': 'Improve Devtools',
        'description': 'Upgrade the tools used for web development',
        'url': 'U_gANjtv28g',
        'todos': ['Watch video', 'Evaluate usability of tools', 'Install viable tools']
    })
    taskcont.create_task({
        'userid': janedoe['_id']['$oid'],
        'title': 'Tech Stacks',
        'description': 'Understand the structure of a tech stack and explore popular stacks in use.',
        'url': 'Sxxw3qtb3_g',
        'todos': ['Watch video', 'Implement the techstack presented in the video']
    })
    taskcont.create_task({
        'userid': janedoe['_id']['$oid'],
        'title': 'Javascript Pro Tips',
        'description': 'Get better at writing JavaScript Code',
        'url': 'Mus_vwhTCq0',
        'todos': ['Watch video']
    })

    return jsonify({'response': 'ok'}), 200

if __name__ == '__main__':
    #populate()
    print(app.url_map)
    app.run()