from os import listdir
from os.path import isfile, join
from typing import List

def list_files(path: str) -> List[str]:
    files = []
    for f in listdir(path):
        p = join(path, f)
        if isfile(p):
            files.append(p)
    return files
