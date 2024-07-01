import os


def get_path_to_file_from_root(path):
    path_to_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', *path)
    return path_to_file
