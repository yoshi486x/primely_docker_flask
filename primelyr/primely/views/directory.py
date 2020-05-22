import configparser
import os
import pathlib

# config = configparser.ConfigParser()
# config.read('config.ini')

# OUTPUT_PATH = config['STORAGE']['TEXT']


def setup_output_dir(child_dir=''):

    output_dir = pathlib.Path(OUTPUT_PATH, child_dir)
    if not os.path.exists(output_dir):
        pathlib.Path(output_dir).mkdir(parents=True)
    else:
        print('Designated directory `{}{}` already exists.'.format(OUTPUT_PATH, child_dir))

if __name__ == "__main__":
    setup_output_dir('')
    setup_output_dir('txt')
    setup_output_dir('json')
    setup_output_dir('report')
    