import os
import pathlib

def get_base_dir_path(file_path):
    """
    input: __file__
    output: Return a path of the package's home directory (three upper parents)"""
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(file_path))))