import configparser
import csv
import os
import pathlib

from primely.views import utils

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
        self.pdf_files = pdf_files
    
    def load_pdf_filenames(self, all_files=list):
        """List all pdf files in designated directory"""
        all_files = []
        pdf_full_dir_path = pathlib.Path(self.base_dir, PDF_DIR_PATH)
        self.pdf_files = os.listdir(pdf_full_dir_path)

        # Extract filename without suffix
        for item in os.listdir(pdf_full_dir_path):
            filename, _ = os.path.splitext(item)
            all_files.append(filename)
        self.all_files = sorted(all_files)
        return self.all_files


def main():
    # inputQueue = InputQueue()
    # filenames = inputQueue.load_pdf_filenames()
    # print('pdf_files:', inputQueue.pdf_files)
    # print('all_files:', inputQueue.all_files)

    reader = PdfReader()
    reader.get_txt_dir

if __name__ == "__main__":
    main()