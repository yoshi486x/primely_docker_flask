import collections
import json
import os
import pathlib

import pprint

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


class RecordingModel(JsonModel):
    """Definition of class that generates ranking model"""

    def __init__(self, filename, json_file=None, db=None):
        JsonModel.__init__(self, filename, json_file)

    def record_data_in_json(self, stack):
        """Export dict_data in json format"""

        data_json = json.dumps(stack, ensure_ascii=False, indent=4)
        with open(self.json_file, 'w') as json_file:
            json_file.write(data_json)

def main(data):
    pass

if __name__ == "__main__":
    main()