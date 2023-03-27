"""File utils"""
from os import listdir
from os.path import isfile, join
from typing import List

def list_files(dir_path: str) -> List[str]:
    files = []
    for file in listdir(dir_path):
        file_path = join(dir_path, file)
        if isfile(file_path) and not file_path.startswith('.'):
            files.append(file_path)
    return files
