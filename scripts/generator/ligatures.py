"""Ligatures feature generator module"""
from typing import List

from .const import IGNORE_PREFIXES, IGNORE_TEMPLATES, REPLACE_TEMPLATES


def render_statements(statements: List[str], prefix: str) -> str:
    """Renders fea statements"""
    return '\n'.join(map(lambda x: f'  {prefix} {x};', statements))

def render_template(template: str, glyphs: List[str]) -> str:
    result = template
    for i, glyph in enumerate(glyphs):
        result = result.replace(str(i + 1), glyph)
    return result

def get_ignore_prefixes(name: str, count: int) -> List[str]:
    ignores: List[str] = []
    tail = ''
    for i in range(count - 1):
        tail += f' {i + 1}'
    for statement, starts in IGNORE_PREFIXES.items():
        for start in starts:
            if name.startswith(start):
                ignores.append(f"{statement} 1' {tail}")
    return ignores

def render_lookup(replace: List[str], ignore: List[str], glyphs: List[str]) -> str:
    name = '_'.join(glyphs)
    template = (
        f"lookup {name}" + " { \n"
        f"{render_statements(ignore, 'ignore sub')}"
        f"{render_statements(replace, 'sub')}"
        "\n} " + f"{name};"
    )
    return render_template(template, glyphs)

def render_ligature(name: str) -> str:
    """Generates an OpenType feature code that replaces characters with ligatures.
    The `name` must be in the format `<glyph>_<glyph>`"""
    glyphs = name.split('_')
    count = len(glyphs)
    ignores = IGNORE_TEMPLATES[count] + get_ignore_prefixes(name, count)
    replaces = REPLACE_TEMPLATES[count]
    return render_lookup(replaces, ignores, glyphs)

def render_ligatures(items: List[str]) -> str:
    """Renders the list of ligatures in the OpenType feature"""
    result = ""
    # For the generated code to work correctly,
    # it is necessary to sort the list in descending order of the number of glyphs
    ligatures = sorted(items, key=lambda x: len(x.split('_')), reverse=True)
    for name in ligatures:
        result += render_ligature(name) + "\n"
    return result
