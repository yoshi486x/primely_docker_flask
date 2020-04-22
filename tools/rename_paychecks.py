import configparser
import os
import pathlib

# import global parameters from config.ini
config = configparser.ConfigParser()
config.read('config.ini')
PDF_DIR_PATH = config['STORAGE']['PDF']


def get_pkg_home_path(file_path):
        """
        input: __file__
        output: Return a path of the package's home directory (three upper parents)"""
        return os.path.abspath(os.path.join(os.path.dirname(file_path), '../'))

def load_pdf_filenames(base_dir):
    """List all pdf files in designated directory"""
    # Get filename 
    all_files = []
    pdf_full_dir_path = pathlib.Path(base_dir, PDF_DIR_PATH)
    pdf_files = os.listdir(pdf_full_dir_path)
    print(pdf_files)

    # Transform filename
    new_name = []
    for file in pdf_files:

        # get_new_name
        ## breakdown name
        tmp = file.split('_')
        if len(tmp) <= 2:
            print('already renamed')
            continue 

        ## create new name
        new_name = '_'.join(tmp[-2:])

        # get_fullpaths
        old_full_path = pathlib.Path(base_dir, PDF_DIR_PATH, file)
        new_full_path = pathlib.Path(base_dir, PDF_DIR_PATH, new_name)
        print('old_full_path:', old_full_path)
        print('new_full_path:', new_full_path)

        # rename
        os.rename(old_full_path, new_full_path)

    return 'success'

def main():
    home_path = get_pkg_home_path(__file__)
    load_pdf_filenames(home_path)


if __name__ == "__main__":
    main()