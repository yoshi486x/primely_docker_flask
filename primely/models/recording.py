import collections
import configparser
import json
import os
import pathlib


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

    def __init__(self, *args, **kwargs):
        JsonModel.__init__(self, **kwargs)

    def record_data_in_json(self, stack):
        """Export dict_data in json format"""

        data_json = json.dumps(stack, ensure_ascii=False, indent=4)
        with open(self.dest_info['file_path'], 'w') as file_path:
            file_path.write(data_json)


if __name__ == "__main__":
    pass