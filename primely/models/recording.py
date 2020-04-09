import collections
import configparser
import json
import os
import pathlib

# import global parameters from config.ini
# config = configparser.ConfigParser()
# config.read('config.ini')
# JSON_DIR_PATH = config['STORAGE']['JSON']

class JsonModel(object):
    # def __init__(self, filename, file_path, dir_path):
    #     self.dir_path = dir_path
    #     if not file_path:
    #         file_path = self.get_json_file_path(filename)
    #     if not os.path.exists(file_path):
    #         pathlib.Path(file_path).touch()
    #     self.filename = filename
    #     self.file_path = file_path
    def __init__(self, *args, **kwargs):
        # print('JMinit:', kwargs)
        if not kwargs['file_path']:
            # Get kwargs from config and update dict
            kwargs = self.get_json_file_path(**kwargs)
            # print('thisKwargs:', kwargs)
        if not os.path.exists(kwargs['file_path']):
            pathlib.Path(kwargs['dir_path']).touch()
        self.dest_info = kwargs
        # print('dest_info:', self.dest_info)

    def get_json_file_path(self, **kwargs):
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
            # json_file_path = pathlib.Path(JSON_DIR_PATH, filename).with_suffix('.json')
            # json_file_path = pathlib.Path(self.dir_path, filename).with_suffix('.json')
            kwargs['file_path'] = pathlib.Path(kwargs['dir_path'], kwargs['filename']).with_suffix('.json')
        return kwargs


class RecordingModel(JsonModel):
    """Definition of class that generates ranking model"""

    # def __init__(self, filename, file_path=None, dir_path=None):
    #     JsonModel.__init__(self, filename, file_path, dir_path)
    def __init__(self, *args, **kwargs):
        # print('RMinit:', kwargs)
        JsonModel.__init__(self, **kwargs)

    def record_data_in_json(self, stack):
        """Export dict_data in json format"""

        data_json = json.dumps(stack, ensure_ascii=False, indent=4)
        # with open(self.file_path, 'w') as file_path:
        with open(self.dest_info['file_path'], 'w') as file_path:
            file_path.write(data_json)


if __name__ == "__main__":
    dest_info = {'filename': '1300_1614120_K_20180425',
     'dir_path': 'data/output/json', 'file_path': None}
    recording = RecordingModel(**dest_info)

    # filename = '1300_1614120_K_20180425'
    # dir_path = 'data/output/json'
    # file_path = None
    # recording = RecordingModel(filename, file_path, dir_path)
