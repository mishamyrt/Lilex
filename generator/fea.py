'''
fea files helpers
'''

def read_file (path: str) -> str:
    with open(path) as file:
        return file.read()

def read_feature (name: str) -> str:
    return read_file(f'./features/{name}.fea')

def read_class (name: str) -> str:
    return read_file(f'./classes/{name}.fea')
