import configparser
import os
import pathlib

try:
    from primely.views import utils
except:
    from primelyr.primely.views import utils

# import global parameters from config.ini
config = configparser.ConfigParser()
config.read('config.ini')
PDF_DIR_PATH = config['STORAGE']['PDF']


class InputQueue(object):
    def __init__(self, base_dir=None, all_files=None, pdf_files=None):
        if not base_dir:
            base_dir = utils.get_base_dir_path(__file__)
        self.base_dir = base_dir
        self.all_files = all_files
        if not pdf_files:
            pdf_files = self.load_pdf_filenames()
        self.pdf_files = pdf_files
    
    def load_pdf_filenames(self):
        """List all pdf files in designated directory"""

        pdf_full_dir_path = pathlib.Path(self.base_dir, PDF_DIR_PATH)
        return os.listdir(pdf_full_dir_path)

    def extract_filenames(self, all_files=[]):
        """Extract filename without suffix"""

        for item in self.pdf_files:
            filename, _ = os.path.splitext(item)
            all_files.append(filename)
        self.all_files = sorted(all_files)

    def get_filename_list(self):
        return self.all_files


def main():
    # inputQueue = InputQueue()
    # filenames = inputQueue.load_pdf_filenames()
    # print('pdf_files:', inputQueue.pdf_files)
    # print('all_files:', inputQueue.all_files)
    pass

if __name__ == "__main__":
    main()