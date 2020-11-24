"""
Glyphs.app format processor
"""

import re
from typing import Union, List, Dict, Tuple

convert_nl = lambda x: x.replace('\n', "\\012")

# Determine minimum indentation (first line doesn't count):
class GlyphsFile:
    glyphs: List[str] = []
    __raw: str = ''
    __path: str
    __features: Dict[str, str]
    __classes: Dict[str, str]

    def __init__ (self, path: str):
        with open(path) as file:
            for line in file:
                self.__raw += f'{line}'
                name = self.__find_glyph_name(line)
                if name is not None:
                    self.glyphs.append(name)
        self.__path = path
        self.__features = self.__read_list('features')
        self.__classes = self.__read_list('classes')

    def flush (self):
        file = open(self.__path, 'w')
        file.write(self.__raw)

    def set_feature (self, name, value):
        self.__features[name] = f'"{convert_nl(value)}"'
        self.__write_list('features', self.__features)

    def set_class (self, name, value):
        self.__classes[name] = f'"{convert_nl(value)}"'
        self.__write_list('classes', self.__classes)

    @property
    def ligatures(self):
        return list(
            map(lambda x: x.replace('.liga', ''),
                filter(lambda x: x.endswith('.liga'), self.glyphs)))

    def __find_glyph_name(self, line: str) -> Union[str, None]:
        result = re.match(r'glyphname = (.*);', line)
        if result is None:
            return None
        return result.group(1)

    def __read_fields (self, field: str, text_slice: str) -> List[str]:
        pattern = re.compile(rf'{field} = (.*)', re.M)
        values: List[str] = []
        for value_match in pattern.finditer(text_slice):
            values.append(value_match.group(1)[:-1])
        return values

    def __find_definition_index (self, field: str, prefix = '') -> Tuple:
        start_index = self.__raw.index(f"{field} = {prefix}")
        end_index = self.__raw.index(');', start_index)
        return (start_index, end_index + 2)

    def __write_list (self, field: str, value: Dict[str, str]):
        start, end = self.__find_definition_index(field)
        list_str = ''
        for name, code in value.items():
            list_str += (
                '{\n'
                f'code = {code};\n'
                f'name = {name};\n'
                '},\n'
            )
        self.__raw = ''.join((
            self.__raw[:start],
            f'{field} = (\n',
            f'{list_str[:-2]}\n'
            ');',
            self.__raw[end:]
        ))

    def __read_list (self, field: str):
        start, end = self.__find_definition_index(field, prefix='(')
        text_slice = self.__raw[start:end + 2]
        keys = self.__read_fields('name', text_slice)
        values = self.__read_fields('code', text_slice)

        if len(keys) != len(values):
            raise Exception('Keys and values count differs')
        return dict(zip(keys, values))
