import configparser
import json
import os
import pathlib

try:
    from primely.models import visualizing
except:
    from primelyr.primely.models import visualizing

# import global parameters from config.ini
config = configparser.ConfigParser()
config.read('config.ini')
REPORT_DIR_PATH = config['STORAGE']['REPORT']
REPORT_FILENAME = config['FILENAME']['REPORT']

def get_json_timechart():
    json_loader = visualizing.JsonLoaderModel(REPORT_FILENAME, REPORT_DIR_PATH)
    return json_loader.dict_data

if __name__ == "__main__":
    get_json_timechart()

