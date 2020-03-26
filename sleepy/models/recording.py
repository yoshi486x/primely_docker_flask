import collections
import json
import os
import pprint
import pathlib

import pymongo

from pymongo import MongoClient

CLIENT_HOST = 'mongodb://localhost:27017/'
CLIENT_NAME = 'test_database'
JSON_DIR_PATH = 'data/output/json'


class JsonModel(object):
    def __init__(self, filename, json_file):
        if not json_file:
            json_file = self.get_json_file_path(filename)
        if not os.path.exists(json_file):
            pathlib.Path(json_file).touch()
        self.filename = filename
        self.json_file = json_file

    def get_json_file_path(self, filename):
        """Set json file path.
        Use json path if set in settings, otherwise use default.
        
        :type filename: str
        :rtype json_file_path: str
        """
        json_file_path = None
        try:
            import settings
            if settings.JSON_FILE_PATH:
                json_file_path = settings.JSON_FILE_PATH
        except ImportError:
            pass

        if not json_file_path:
            json_file_path = pathlib.Path(JSON_DIR_PATH, filename).with_suffix('.json')
        return json_file_path

class MongoModel(object):
    def __init__(self, db):
        self.db = db

    def get_mongo_profile(self):
        """Define DB. Check if db is active.
        :rtype: Boolen
        """
        try:
            client = MongoClient(host=CLIENT_HOST, serverSelectionTimeoutMS=100)
            client.server_info()
            self.db = client[CLIENT_NAME]
            return True
        except pymongo.errors.ServerSelectionTimeoutError as error:
            return False


class RecordingModel(JsonModel, MongoModel):
    """Definition of class that generates ranking model to write to MongoDB"""

    def __init__(self, filename, mongo_status, json_file=None, db=None):
        JsonModel.__init__(self, filename, json_file)
        MongoModel.__init__(self, db)
        if mongo_status:
            self.get_mongo_profile()

    def record_data_to_mongo(self, dict_data):
        """Store dict_data to MongoDB"""

        # Insert data to DB
        stack = dict_data
        db_stacks = self.db.stacks
        stack_id = db_stacks.insert_one(stack).inserted_id

        # Print to see the inserted data
        # print(stack_id, type(stack_id))
        # pp.pprint(db_stacks.find_one({'_id': stack_id}))

    def record_data_in_json(self, stack):
        """Export dict_data in json format"""

        data_json = json.dumps(stack, ensure_ascii=False, indent=4)
        with open(self.json_file, 'w') as json_file:
            json_file.write(data_json)

def main(data):
    pass

if __name__ == "__main__":
    main()