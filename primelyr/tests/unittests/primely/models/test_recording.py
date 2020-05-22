import os
import pathlib
import unittest

from context import recording

"""TODO not complete"""
class SolutionTest(unittest.TestCase):

    def setUp(self):
        print('setup')
        self.recorder = recording.RecordingModel()

    def record_data_in_json(self):
        # test case 1
        self.assertIsNone(self.recorder.record_data_in_json())

    # def test_extract_filenames(self):
    #     # test case 2
    #     self.assertIsNone(self.input_queue.extract_filenames())

    # def test_get_filename_list(self):
    #     # test case 3
    #     self.assertIsNone(self.input_queue.get_filename_list())

    def tearDown(self):
        print('clean up')
        del self.input_queue


if __name__ == "__main__":
    unittest.main()