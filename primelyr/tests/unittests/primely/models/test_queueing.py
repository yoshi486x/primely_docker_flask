import os
import pathlib
import unittest

from context import queueing

class SolutionTest(unittest.TestCase):

    def setUp(self):
        print('setup')
        self.input_queue = queueing.InputQueue()

    def test_load_pdf_filenames(self):
        # test case 1
        self.assertIsNotNone(self.input_queue.load_pdf_filenames())

    def test_extract_filenames(self):
        # test case 2
        self.assertIsNone(self.input_queue.extract_filenames())

    def test_get_filename_list(self):
        # test case 3
        self.assertIsNone(self.input_queue.get_filename_list())

    def tearDown(self):
        print('clean up')
        del self.input_queue


if __name__ == "__main__":
    unittest.main()