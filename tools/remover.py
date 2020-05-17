import configparser
import os
import pathlib
import shutil

# import global parameters from config.ini
config = configparser.ConfigParser()
config.read('config.ini')
PDF_DIR_PATH = config['STORAGE']['PDF']
REPORT_DIR_PATH = config['STORAGE']['REPORT']
REPORT_FILENAME = config['FILENAME']['REPORT']

def remove_report():
    file_path = pathlib.Path(REPORT_DIR_PATH, REPORT_FILENAME)
    print(file_path)

    try:
        if os.path.exists(file_path):
            print('exist')
            os.remove(file_path)
            print(f'removed {file_path}')
        else:
            print(f'The file does not exist: {file_path}')
    except Exception as e:
        print(f'Failed to delete {file_path}. Reason: {e}')
    else:
        return True

    return

def remove_pdf():
    folder = PDF_DIR_PATH
    for filename in os.listdir(folder):
        file_path = pathlib.Path(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}' )

    return True


if __name__ == "__main__":
    remove_pdf()