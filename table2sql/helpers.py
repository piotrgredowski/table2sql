import os


def get_sibling_file_path(base_file: str, target_file_name: str):
    return os.path.join(os.path.dirname(base_file), target_file_name)
