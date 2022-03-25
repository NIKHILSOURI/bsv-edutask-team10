# coding=utf-8
import json
from bson import json_util
from bson.objectid import ObjectId


class Video:

    def __init__(self, database):
        self.database = database
        self.collection = self.database.video

    def create(self, data):
        video = {
            'url': data.get('url'),
            'taskid': ObjectId(data.get('taskid'))
        }

        inserted_id = self.collection.insert_one(video).inserted_id
        video = self.collection.find_one({ '_id': ObjectId(inserted_id) })
        
        return self.to_json(video)

    # obtain a video by id
    def get_video(self, object_id):
        video = self.collection.find_one({ '_id': ObjectId(object_id)})
        return self.to_json(video)

    def get_video_of_task(self, task_id: str):
        video = self.collection.find_one({'_id': ObjectId(task_id)})
        return video

    #def update(self):
    #    pass

    #def delete(self):
    #    pass

    def to_json(self, data):
        return json.loads(json_util.dumps(data))
