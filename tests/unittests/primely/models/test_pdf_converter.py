import os
import pathlib
import unittest

from context import pdf_converter

class SolutionTest(unittest.TestCase):

    def setUp(self):
        print('setup')
        filename = 'K_20180425'
        self.pdf_converter = pdf_converter.PdfReader(filename)
        self.root_path = self.pdf_converter.base_dir

    def test_get_pdf_dir(self):
        # test case 1
        answer = pathlib.Path(self.root_path, 'data/pdf/K_20180425.pdf')
        self.assertEqual(
            self.pdf_converter.get_pdf_dir(), answer)

    # @unittest.skip('skip!')
    def test_get_txt_dir(self):
        # test case 2
        answer = pathlib.Path(self.root_path, 'data/output/temp/K_20180425.txt')
        self.assertEqual(
            self.pdf_converter.get_txt_dir(), answer)

    # @unittest.skip('skip!')
    # @unittest.skipIf(release_name=='DEBUG')
    def test_convert_pdf_to_txt(self):
        # test case 3
        input_file_path = pathlib.Path(self.root_path, '/data/pdf/K_20180425.pdf')
        output_file_path = pathlib.Path(self.root_path, '/data/output/temp/K_20180425.txt')
        answer = 'success'
        self.assertEqual(
            self.pdf_converter.convert_pdf_to_txt(input_file_path, output_file_path),
            answer)

    def tearDown(self):
        print('clean up')
        del self.pdf_converter


if __name__ == "__main__":
    unittest.main()