'''
Ligatures feature generator
'''

from typing import List

ignore_exceptions = {
    'slash_asterisk': [
        "slash' asterisk slash",
        "asterisk slash' asterisk"
    ],
    'asterisk_slash': [
        "slash asterisk' slash",
        "asterisk' slash asterisk"
    ],
    'asterisk_asterisk': [
        "slash asterisk' asterisk",
        "asterisk' asterisk slash"
    ],
    "asterisk_asterisk_asterisk": [
        "slash asterisk' asterisk asterisk",
        "asterisk' asterisk asterisk slash",
    ],
    "colon_colon": [
        "colon' colon [less greater]",
        "[less greater] colon' colon"
    ],
    "less_less": ["less' less [asterisk plus dollar]"],
    "equal_equal": [
        "bracketleft equal' equal",
        "equal' equal bracketright",
        "equal [colon exclam] equal' equal",
        "[less greater bar slash] equal' equal",
        "equal' equal [less greater bar slash]",
        "equal' equal [colon exclam] equal"
    ],
    "equal_equal_equal": [
        "equal [colon exclam] equal' equal equal",
        "[less greater bar slash] equal' equal equal",
        "equal' equal equal [less greater bar slash]",
        "equal' equal equal [colon exclam] equal",
        "bracketleft equal' equal equal",
        "equal' equal equal bracketright"
    ],
    "colon_equal": ["equal colon' equal"],
    "exclam_equal": ["equal exclam' equal"],
    "exclam_equal_equal": ["equal exclam' equal equal"],
    "less_equal": [
        "equal less' equal",
        "less' equal [less greater bar colon exclam slash]"
    ],
    "greater_equal": [
        "equal greater' equal",
        "greater' equal [less greater bar colon exclam slash]"
    ],
    "greater_greater": [
        "[hyphen equal] greater' greater",
        "greater' greater hyphen",
        "[asterisk plus dollar] greater' greater",
        "greater' greater equal [equal less greater bar colon exclam slash]"
    ],
    "bar_bar": [
        "[hyphen equal] bar' bar",
        "bar' bar hyphen",
        "bar' bar equal [equal less greater bar colon exclam slash]"
    ],
    "slash_slash": [
        "equal slash' slash",
        "slash' slash equal"
    ],
    "hyphen_hyphen": [
        "[less greater bar] hyphen' hyphen",
        "hyphen' hyphen [less greater bar]"
    ],
}

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

# Replacemnt ignore templates map
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

# Replacemnt templates map
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

def render_ligature_lookups (ligatures: List[str]) -> str:
    result = ""
    for name in ligatures:
        glyphs = name.split('_')
        lenght = len(glyphs)
        ignores = ignore_templates[lenght] + get_ignore_prefixes(name, lenght)
        replaces = replace_templates[lenght]
        result += render_lookup(replaces, ignores, glyphs) + "\n"
    return result
