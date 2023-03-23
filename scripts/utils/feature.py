from re import search
from os.path import basename

def format_feature (feature: str) -> str:
    result = search(r'Name:(.*)', feature)
    try:
        name = result.group(1).strip()
        return (
            'featureNames {\n'
            f'name 3 1 0x0409 "{name}";\n'
            f'name 1 0 0 "{name}";\n'
            '};\n' + feature
        )
    except AttributeError:
        return feature

class OTFeature:
    _content: str
    name: str = None

    def __init__(self, name: str = None, path: str = None) -> None:
        if name is None:
            self.name = basename(path).split('.')[0]
        else:
            self.name = name
        if path is not None:
            self._load_from_file(path)

    def _load_from_file(self, path: str) -> None:
        with open(path, mode="r", encoding="utf-8") as file:
            self._content = self._format(file.read())

    def _format(self, content: str) -> str:
        if self.name.startswith("ss"):
            return format_feature(content)
        return content

    def __str__(self) -> str:
        return self._content

class OTClass(OTFeature):
    def _format(self, content: str) -> str:
        return content