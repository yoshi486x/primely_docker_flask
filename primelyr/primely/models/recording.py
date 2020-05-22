import collections
import configparser
import json
import os
import pathlib

try:
    from primely.views import utils
except:
    from primelyr.primely.views import utils

# import global parameters from config.ini
config = configparser.ConfigParser()
config.read('config.ini')
OUTPUT_DIR_PATH = config['STORAGE']['JSON']


class JsonModel(object):

    def __init__(self, *args, **kwargs):
        
        if not kwargs['file_path']:
            # Get kwargs from config and update dict
            kwargs = self.get_json_file_path(**kwargs)
        if not os.path.exists(kwargs['file_path']):
            pathlib.Path(kwargs['dir_path']).touch()
        self.dest_info = kwargs

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
            kwargs['file_path'] = pathlib.Path(kwargs['dir_path'], kwargs['filename']).with_suffix('.json')
        return kwargs


class RecordingModel(JsonModel):
    # TODO Write header doc more cleary
    """Definition of class that generates ranking model
    :type dest_info: dict
    :rtype: None

    dest_info = {
            'filename': filename,
            'dir_path': config['STORAGE']['JSON'],
            'file_path': None
        }
    """

    # def __init__(self, filename=None, base_dir=None, *args, **kwargs):
    def __init__(self, *args, **kwargs):
        JsonModel.__init__(self, **kwargs)
        # self.filename = filename
        # if not base_dir:
        #     base_dir = utils.get_base_dir_path(__file__)
        # self.base_dir = base_dir

    def get_json_dir(self, suffix='.json'):
        """Organize output json path info"""
        output_full_dir_path = pathlib.Path(self.base_dir, OUTPUT_DIR_PATH)
        print('############:', output_full_dir_path)
        utils.setup_output_dir(output_full_dir_path)
        return pathlib.Path(output_full_dir_path, self.filename).with_suffix(suffix)

    def record_data_in_json(self, stack):
        """Export dict_data in json format"""

        data_json = json.dumps(stack, ensure_ascii=False, indent=4)
        output_json_path = self.dest_info['file_path']

        with open(output_json_path, 'w') as file_path:
            file_path.write(data_json)

    def record_dict_in_json(self, dict_data, output_path):
        """Export dict_data in json format"""

        data_json = json.dumps(dict_data, ensure_ascii=False, indent=4)
        with open(output_path, 'w') as file_path:
            file_path.write(data_json)


if __name__ == "__main__":
    pass