import os


def get_path_to_file_from_root(path):
    path_to_file = os.path.normpath(os.path.dirname(os.path.abspath(os.path.join(__file__, '..'))) + "\\" + path)
    return path_to_file
