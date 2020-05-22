import configparser
import os
import pathlib
import subprocess
import sys

try:
    from primely.views import utils
except:
    from primelyr.primely.views import utils

# import global parameters from config.ini
config = configparser.ConfigParser()
config.read('config.ini')
OUTPUT_DIR_PATH = config['STORAGE']['TEXT']
PDF_DIR_PATH = config['STORAGE']['PDF']

EXEC_CMD = 'pdf2txt.py'


class PdfReader(object):
    def __init__(self, filename, base_dir=None):
        self.filename = filename
        if not base_dir:
            base_dir = utils.get_base_dir_path(__file__)
        self.base_dir = base_dir

    def get_pdf_dir(self, suffix='.pdf'):
        """Organize input pdf path info"""
        # print('filename:', filename)
        input_full_dir_path = pathlib.Path(self.base_dir, PDF_DIR_PATH)
        return pathlib.Path(input_full_dir_path, self.filename).with_suffix(suffix)

    def get_txt_dir(self, suffix='.txt'):
        """Organize output txt path info"""
        output_full_dir_path = pathlib.Path(self.base_dir, OUTPUT_DIR_PATH)
        # if not os.path.exists(output_full_dir_path):
        utils.setup_output_dir(output_full_dir_path)
        return pathlib.Path(output_full_dir_path, self.filename).with_suffix(suffix)

    # TODO Set classmethod regarding pdf and txt imports
    def convert_pdf_to_txt(self, input_file, output_file):
        """Call pdf2text.py
        :type input_file :str
        :type output_file :str
        """
        # TODO Error handle this process call
        try:
            subprocess.call([EXEC_CMD, '-V', '-o', str(output_file), str(input_file)])
        except:
            raise

        return 'success'


def main():
    # inputQueue = InputQueue()
    # filenames = inputQueue.load_pdf_filenames()
    # print('pdf_files:', inputQueue.pdf_files)
    # print('all_files:', inputQueue.all_files)

    reader = PdfReader()
    reader.get_txt_dir

if __name__ == "__main__":
    main()