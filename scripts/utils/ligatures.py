"""Ligatures feature generator module"""

from typing import List

ignore_prefixes = {
    'parenleft question': [
        'colon',
        'equal'
        'exclaim'
    ],
    'less question': ['equal'],
    'parenleft question less': [
        'equal',
        'exclaim'
    ],
}

# Replacement ignore templates map
# ignore sub
ignore_templates = {
    2: [
        "1  1' 2",
        "1' 2  2"
    ],
    3: [
        "1  1' 2  3",
        "1' 2  3  3"
    ],
    4: [
        "1  1' 2  3  4",
        "1' 2  3  4  4"
    ]
}

# Replacement templates map
# sub
replace_templates = {
    2: [
        "LIG 2' by 1_2.liga",
        "1'  2  by LIG"
    ],
    3: [
        "LIG LIG 3' by 1_2_3.liga",
        "LIG 2'  3  by LIG",
        "1'  2   3  by LIG"
    ],
    4: [
        "LIG LIG LIG 4' by 1_2_3_4.liga",
        "LIG LIG 3'  4  by LIG",
        "LIG 2'  3   4  by LIG",
        "1'  2   3   4  by LIG"
    ]
}

def render_statements (statements: List[str], prefix: str) -> str:
    return '\n'.join(map(lambda x: f'  {prefix} {x};', statements))

def render_template (template: str, glyphs: List[str]) -> str:
    for i, _ in enumerate(glyphs):
        template = template.replace(str(i + 1), glyphs[i])
    return template

def render_lookup (replace: List[str], ignore: List[str], glyphs: List[str]) -> str:
    name = '_'.join(glyphs)
    template = (
        f"lookup {name}" + " { \n"
        f"{render_statements(ignore, 'ignore sub')}"
        f"{render_statements(replace, 'sub')}"
        "\n} " + f"{name};"
    )
    return render_template(template, glyphs)

def get_ignore_prefixes(name: str, length: int) -> List[str]:
    ignores: List[str] = []
    tail = ''
    for i in range(length - 1):
        tail += f' {i + 1}'
    for statement, starts in ignore_prefixes.items():
        for start in starts:
            if name.startswith(start):
                ignores.append(f"{statement} 1' {tail}")
    return ignores

def ligature_lookups (ligatures: List[str]) -> str:
    result = ""
    for name in ligatures:
        glyphs = name.split('_')
        length = len(glyphs)
        ignores = ignore_templates[length] + get_ignore_prefixes(name, length)
        replaces = replace_templates[length]
        result += render_lookup(replaces, ignores, glyphs) + "\n"
    return result
