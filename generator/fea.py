
'''
fea files helpers
'''

from re import search

ignore_name = [
    'calt',
    'mark',
    'aalt',
    'frac'
]

def read_file (path: str) -> str:
    with open(path) as file:
        return file.read()

def get_feature_name (feature: str) -> str:
    result = search(r'Name:(.*)', feature)
    name = result.group(1).strip()
    return (
        'featureNames {\n'
        f'name 3 1 0x0409 "{name}";\n'
        f'name 1 0 0 "{name}";\n'
        '};\n'
    )

def read_feature (name: str) -> str:
    content = read_file(f'./features/{name}.fea')
    if name.split('/')[0] in ignore_name:
        return content
    return get_feature_name(content) + content

def read_class (name: str) -> str:
    return read_file(f'./classes/{name}.fea')
