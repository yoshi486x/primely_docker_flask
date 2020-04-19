import os
import pathlib
import unittest

from context import pdf_reader


class SolutionTest(unittest.TestCase):

    def setUp(self):
        print('setup')
        self.pdf_reader = pdf_reader.PdfReader()
        self.root_path = self.pdf_reader.base_dir

    def test_get_pdf_dir(self):
        # test case 1
        filename = '1300_1614120_K_20180425'
        answer = pathlib.Path(self.root_path, 'data/pdf/1300_1614120_K_20180425.pdf')
        self.assertEqual(
            self.pdf_reader.get_pdf_dir(filename), answer)

    # @unittest.skip('skip!')
    def test_get_txt_dir(self):
        # test case 2
        filename = '1300_1614120_K_20180425'
        answer = pathlib.Path(self.root_path, 'data/output/temp/1300_1614120_K_20180425.txt')
        self.assertEqual(
            self.pdf_reader.get_txt_dir(filename), answer)

    # @unittest.skip('skip!')
    # @unittest.skipIf(release_name=='DEBUG')
    def test_convert_pdf_to_txt(self):
        # test case 3
        input_file_path = pathlib.Path(self.root_path, '/data/pdf/1300_1614120_K_20180425.pdf')
        output_file_path = pathlib.Path(self.root_path, '/data/output/temp/1300_1614120_K_20180425.txt')
        answer = 'success'
        self.assertEqual(
            self.pdf_reader.convert_pdf_to_txt(input_file_path, output_file_path),
            answer)

    def tearDown(self):
        print('clean up')
        del self.pdf_reader


if __name__ == "__main__":
    unittest.main()